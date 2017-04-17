# Copyright 2017 Google Inc. All Rights Reserved.
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
"""Patches the settings of a Cloud SQL database."""

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.sql import flags
from googlecloudsdk.core import log


class _Result(object):
  """Run() method result object."""

  def __init__(self, new, old):
    self.new = new
    self.old = old


class _BasePatch(object):
  """Patches the settings of a Cloud SQL database."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Please add arguments in alphabetical order except for no- or a clear-
    pair for that argument which can follow the argument itself.
    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """

    flags.CHARSET_FLAG.AddToParser(parser)
    flags.COLLATION_FLAG.AddToParser(parser)
    flags.DATABASE_NAME_FLAG.AddToParser(parser)
    flags.INSTANCE_FLAG.AddToParser(parser)
    parser.add_argument(
        '--diff',
        action='store_true',
        help='Show what changed as a result of the patch.')

  def Format(self, args):
    if args.diff:
      return 'diff(old, new)'
    fmt = self.ListFormat(args)
    return 'table(new:format="{fmt}")'.format(fmt=fmt)

  def Run(self, args):
    """Patches settings of a Cloud SQL database using the patch api method.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      A dict object representing the operations resource describing the patch
      operation if the patch was successful.
    Raises:
      HttpException: A http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """
    client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    instance_ref = client.resource_parser.Parse(
        args.instance, collection='sql.instances')

    original_database_resource = sql_client.databases.Get(
        sql_messages.SqlDatabasesGetRequest(
            database=args.database,
            project=instance_ref.project,
            instance=instance_ref.instance))

    patch_database = sql_messages.Database(
        project=instance_ref.project,
        instance=instance_ref.instance,
        name=args.database)

    if hasattr(args, 'collation'):
      patch_database.collation = args.collation

    if hasattr(args, 'charset'):
      patch_database.charset = args.charset

    operation_ref = None

    result_operation = sql_client.databases.Patch(
        sql_messages.SqlDatabasesPatchRequest(
            database=args.database,
            databaseResource=patch_database,
            project=instance_ref.project,
            instance=instance_ref.instance))

    operation_ref = client.resource_parser.Create(
        'sql.operations',
        operation=result_operation.name,
        project=instance_ref.project)

    operations.OperationsV1Beta4.WaitForOperation(
        sql_client, operation_ref, 'Patching Cloud SQL database')

    log.UpdatedResource(args.database, 'database')

    changed_database_resource = sql_client.databases.Get(
        sql_messages.SqlDatabasesGetRequest(
            database=args.database,
            project=instance_ref.project,
            instance=instance_ref.instance))
    return _Result(changed_database_resource, original_database_resource)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class PatchBeta(_BasePatch, base.Command):
  """Patches the settings of a Cloud SQL database."""
