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
"""Restarts a Cloud SQL instance."""

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.api_lib.sql import validate
from googlecloudsdk.calliope import base
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


class _BaseRestart(object):
  """Restarts a Cloud SQL instance."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    base.ASYNC_FLAG.AddToParser(parser)
    parser.add_argument(
        'instance',
        completion_resource='sql.instances',
        help='Cloud SQL instance ID.')


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Restart(_BaseRestart, base.Command):
  """Restarts a Cloud SQL instance."""

  def Run(self, args):
    """Restarts a Cloud SQL instance.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      A dict object representing the operations resource describing the restart
      operation if the restart was successful.
    Raises:
      HttpException: A http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """
    client = api_util.SqlClient(api_util.API_VERSION_FALLBACK)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    validate.ValidateInstanceName(args.instance)
    instance_ref = client.resource_parser.Parse(
        args.instance, collection='sql.instances')

    console_io.PromptContinue(
        message='The instance will shut down and start up again immediately if '
        'its activation policy is "always." If "on demand," the instance will '
        'start up again when a new connection request is made.',
        default=True,
        cancel_on_no=True)

    result = sql_client.instances.Restart(
        sql_messages.SqlInstancesRestartRequest(
            project=instance_ref.project,
            instance=instance_ref.instance))

    operation_ref = client.resource_parser.Create(
        'sql.operations',
        operation=result.operation,
        project=instance_ref.project,
        instance=instance_ref.instance,
    )

    if args.async:
      return sql_client.operations.Get(
          sql_messages.SqlOperationsGetRequest(
              project=operation_ref.project,
              instance=operation_ref.instance,
              operation=operation_ref.operation))

    operations.OperationsV1Beta3.WaitForOperation(
        sql_client, operation_ref, 'Restarting Cloud SQL instance')

    log.status.write(
        'Restarted [{resource}].\n'.format(resource=instance_ref))


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class RestartBeta(_BaseRestart, base.Command):
  """Restarts a Cloud SQL instance."""

  def Run(self, args):
    """Restarts a Cloud SQL instance.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      A dict object representing the operations resource describing the restart
      operation if the restart was successful.
    Raises:
      HttpException: A http error response was received while executing api
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

    console_io.PromptContinue(
        message='The instance will shut down and start up again immediately if '
        'its activation policy is "always." If "on demand," the instance will '
        'start up again when a new connection request is made.',
        default=True,
        cancel_on_no=True)

    result_operation = sql_client.instances.Restart(
        sql_messages.SqlInstancesRestartRequest(
            project=instance_ref.project,
            instance=instance_ref.instance))

    operation_ref = client.resource_parser.Create(
        'sql.operations',
        operation=result_operation.name,
        project=instance_ref.project)

    if args.async:
      return sql_client.operations.Get(
          sql_messages.SqlOperationsGetRequest(
              project=operation_ref.project,
              instance=operation_ref.instance,
              operation=operation_ref.operation))

    operations.OperationsV1Beta4.WaitForOperation(
        sql_client, operation_ref, 'Restarting Cloud SQL instance')

    log.status.write(
        'Restarted [{resource}].\n'.format(resource=instance_ref))
