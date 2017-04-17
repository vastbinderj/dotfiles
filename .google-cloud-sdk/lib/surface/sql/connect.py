# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Connects to a Cloud SQL instance."""

import datetime

from apitools.base.protorpclite import util as protorpc_util
from apitools.base.py import exceptions as apitools_exceptions

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.api_lib.sql import constants
from googlecloudsdk.api_lib.sql import network
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.api_lib.sql import validate
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import execution_utils
from googlecloudsdk.core.util import files
from googlecloudsdk.core.util import retry
from googlecloudsdk.core.util import text


def _WhitelistClientIP(instance_ref, sql_client, sql_messages, resources,
                       minutes=5):
  """Add CLIENT_IP to the authorized networks list.

  Makes an API call to add CLIENT_IP to the authorized networks list.
  The server knows to interpret the string CLIENT_IP as the address with which
  the client reaches the server. This IP will be whitelisted for 1 minute.

  Args:
    instance_ref: resources.Resource, The instance we're connecting to.
    sql_client: apitools.BaseApiClient, A working client for the sql version
        to be used.
    sql_messages: module, The module that defines the messages for the sql
        version to be used.
    resources: resources.Registry, The registry that can create resource refs
        for the sql version to be used.
    minutes: How long the client IP will be whitelisted for, in minutes.

  Returns:
    string, The name of the authorized network rule. Callers can use this name
    to find out the IP the client reached the server with.
  Raises:
    HttpException: An http error response was received while executing api
        request.
    ToolException: Server did not complete the whitelisting operation in time.
  """
  datetime_now = datetime.datetime.now(
      protorpc_util.TimeZoneOffset(datetime.timedelta(0)))

  acl_name = 'sql connect at time {0}'.format(datetime_now)
  user_acl = sql_messages.AclEntry(
      name=acl_name,
      expirationTime=datetime_now + datetime.timedelta(minutes=minutes),
      value='CLIENT_IP')

  try:
    original = sql_client.instances.Get(
        sql_messages.SqlInstancesGetRequest(
            project=instance_ref.project,
            instance=instance_ref.instance))
  except apitools_exceptions.HttpError as error:
    raise exceptions.HttpException(error)

  original.settings.ipConfiguration.authorizedNetworks.append(user_acl)
  patch_request = sql_messages.SqlInstancesPatchRequest(
      databaseInstance=original,
      project=instance_ref.project,
      instance=instance_ref.instance)
  result = sql_client.instances.Patch(patch_request)

  operation_ref = resources.Create(
      'sql.operations',
      operation=result.name,
      project=instance_ref.project)
  message = ('Whitelisting your IP for incoming connection for '
             '{0} {1}'.format(minutes, text.Pluralize(minutes, 'minute')))

  operations.OperationsV1Beta4.WaitForOperation(
      sql_client, operation_ref, message)

  return acl_name


def _GetClientIP(instance_ref, sql_client, acl_name):
  """Retrieves given instance and extracts its client ip."""
  instance_info = sql_client.instances.Get(
      sql_client.MESSAGES_MODULE.SqlInstancesGetRequest(
          project=instance_ref.project,
          instance=instance_ref.instance))
  networks = instance_info.settings.ipConfiguration.authorizedNetworks
  client_ip = None
  for net in networks:
    if net.name == acl_name:
      client_ip = net.value
      break
  return instance_info, client_ip


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class Connect(base.Command):
  """Connects to a Cloud SQL instance."""

  detailed_help = {
      'EXAMPLES': """\
          To connect to a Cloud SQL instance, run:

            $ {command} my-instance --user=root
          """,
  }

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use it to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    parser.add_argument(
        'instance',
        completion_resource='sql.instances',
        help='Cloud SQL instance ID.')

    parser.add_argument(
        '--user', '-u',
        required=False,
        help='Cloud SQL instance user to connect as.')

  def Run(self, args):
    """Connects to a Cloud SQL instance.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      If no exception is raised this method does not return. A new process is
      started and the original one is killed.
    Raises:
      HttpException: An http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """
    client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    validate.ValidateInstanceName(args.instance)
    instance_ref = client.resource_parser.Parse(
        args.instance, collection='sql.instances')

    acl_name = _WhitelistClientIP(instance_ref, sql_client, sql_messages,
                                  client.resource_parser)

    # Get the client IP that the server sees. Sadly we can only do this by
    # checking the name of the authorized network rule.
    retryer = retry.Retryer(max_retrials=2, exponential_sleep_multiplier=2)
    try:
      instance_info, client_ip = retryer.RetryOnResult(
          _GetClientIP,
          [instance_ref, sql_client, acl_name],
          should_retry_if=lambda x, s: x[1] is None,  # client_ip is None
          sleep_ms=500)
    except retry.RetryException:
      raise exceptions.ToolException('Could not whitelist client IP. Server '
                                     'did not reply with the whitelisted IP.')

    # Check for the mysql or psql executable based on the db version.
    db_type = instance_info.databaseVersion.split('_')[0]
    exe_name = constants.DB_EXE.get(db_type, 'mysql')
    exe = files.FindExecutableOnPath(exe_name)
    if not exe:
      raise exceptions.ToolException(
          '{0} client not found.  Please install a {1} client and make sure '
          'it is in PATH to be able to connect to the database instance.'
          .format(exe_name.title(), exe_name))

    # Check the version of IP and decide if we need to add ipv4 support.
    ip_type = network.GetIpVersion(client_ip)
    if ip_type == network.IP_VERSION_4:
      if instance_info.settings.ipConfiguration.ipv4Enabled:
        ip_address = instance_info.ipAddresses[0].ipAddress
      else:
        # TODO(b/36049930): ask user if we should enable ipv4 addressing
        message = ('It seems your client does not have ipv6 connectivity and '
                   'the database instance does not have an ipv4 address. '
                   'Please request an ipv4 address for this database instance.')
        raise exceptions.ToolException(message)
    elif ip_type == network.IP_VERSION_6:
      ip_address = instance_info.ipv6Address
    else:
      raise exceptions.ToolException('Could not connect to SQL server.')

    # We have everything we need, time to party!
    flags = constants.EXE_FLAGS[exe_name]
    sql_args = [exe_name, flags['hostname'], ip_address]
    if args.user:
      sql_args.extend([flags['user'], args.user])
    sql_args.append(flags['password'])

    execution_utils.Exec(sql_args)
