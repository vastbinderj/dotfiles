# Copyright 2016 Google Inc. All Rights Reserved.
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
"""Deletes a user in a given instance.

Deletes a user in a given instance specified by username and host.
"""

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.sql import flags
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class DeleteBeta(base.DeleteCommand):
  """Deletes a Cloud SQL user in a given instance.

  Deletes a Cloud SQL user in a given instance specified by username and host.
  """

  @staticmethod
  def Args(parser):
    flags.INSTANCE_FLAG.AddToParser(parser)
    flags.USERNAME_FLAG.AddToParser(parser)
    flags.HOST_FLAG.AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    """Lists Cloud SQL users in a given instance.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      SQL user resource iterator.
    Raises:
      HttpException: An http error response was received while executing api
          request.
      ToolException: An error other than an http error occured while executing
          the command.
    """
    client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    project_id = properties.VALUES.core.project.Get(required=True)

    instance_ref = client.resource_parser.Parse(
        args.instance, collection='sql.instances')
    operation_ref = None

    console_io.PromptContinue(
        message='{0}@{1} will be deleted. New connections can no longer be '
        'made using this user. Existing connections are not affected.'.format(
            args.username, args.host),
        default=True,
        cancel_on_no=True)

    result_operation = sql_client.users.Delete(
        sql_messages.SqlUsersDeleteRequest(project=project_id,
                                           instance=args.instance,
                                           name=args.username,
                                           host=args.host))
    operation_ref = client.resource_parser.Create(
        'sql.operations',
        operation=result_operation.name,
        project=instance_ref.project)
    if args.async:
      return sql_client.operations.Get(
          sql_messages.SqlOperationsGetRequest(
              project=operation_ref.project,
              operation=operation_ref.operation))
    operations.OperationsV1Beta4.WaitForOperation(sql_client, operation_ref,
                                                  'Deleting Cloud SQL user')
