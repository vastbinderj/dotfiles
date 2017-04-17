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

"""Lists customizable flags for Google Cloud SQL instances."""

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.calliope import base


def _AddCommonFlags(parser):
  """Adds flags common to all release tracks."""
  parser.display_info.AddFormat("""
    table(
        name,
        type,
        appliesTo.list():label=DATABASE_VERSION,
        allowedStringValues.list():label=ALLOWED_VALUES
      )
    """)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class List(base.ListCommand):
  """List customizable flags for Google Cloud SQL instances."""

  @staticmethod
  def Args(parser):
    _AddCommonFlags(parser)

  def Run(self, unused_args):
    """Lists customizable MySQL flags for Google Cloud SQL instances.

    Args:
      unused_args: argparse.Namespace, The arguments that this command was
          invoked with.

    Returns:
      A dict object that has the list of flag resources if the command ran
      successfully.
    Raises:
      HttpException: A http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """
    client = api_util.SqlClient(api_util.API_VERSION_FALLBACK)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    result = sql_client.flags.List(sql_messages.SqlFlagsListRequest())
    return iter(result.items)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class ListBeta(base.ListCommand):
  """List customizable flags for Google Cloud SQL instances."""

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
    _AddCommonFlags(parser)
    parser.add_argument(
        '--database-version',
        required=False,
        choices=['MYSQL_5_5', 'MYSQL_5_6', 'MYSQL_5_7', 'POSTGRES_9_6'],
        help='Only list flags that apply to the specified database version.',
        hidden='True'  # TODO(b/36057350): unhide the week of GCP Next 2017
    )

  def Run(self, args):
    """List customizable flags for Google Cloud SQL instances.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
      with.

    Returns:
      A dict object that has the list of flag resources if the command ran
      successfully.
    Raises:
      HttpException: A http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """

    client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    result = sql_client.flags.List(
        sql_messages.SqlFlagsListRequest(databaseVersion=args.database_version))
    return iter(result.items)
