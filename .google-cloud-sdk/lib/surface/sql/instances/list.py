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

"""Lists instances in a given project.

Lists instances in a given project in the alphabetical order of the
instance name.
"""

from apitools.base.py import list_pager

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.sql import flags
from googlecloudsdk.core import properties


def _GetUriFromResource(resource):
  """Returns the URI for resource."""
  client = api_util.SqlClient(api_util.API_VERSION_FALLBACK)
  return client.resource_parser.Create(
      'sql.instances', project=resource.project,
      instance=resource.instance).SelfLink()


def _GetUriFromResourceBeta(resource):
  """Returns the URI for resource."""
  client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
  return client.resource_parser.Create(
      'sql.instances', project=resource.project,
      instance=resource.name).SelfLink()


class _BaseList(object):
  """Lists Cloud SQL instances in a given project."""

  def Run(self, args):
    """Lists Cloud SQL instances in a given project.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      SQL instance resource iterator.
    Raises:
      HttpException: An http error response was received while executing api
          request.
      ToolException: An error other than an http error occured while executing
          the command.
    """
    client = self.GetSqlClient()
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    project_id = properties.VALUES.core.project.Get(required=True)

    return list_pager.YieldFromList(
        sql_client.instances,
        sql_messages.SqlInstancesListRequest(project=project_id),
        limit=args.limit)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class List(_BaseList, base.ListCommand):
  """Lists Cloud SQL instances in a given project.

  Lists Cloud SQL instances in a given project in the alphabetical
  order of the instance name.
  """

  @staticmethod
  def Args(parser):
    parser.display_info.AddFormat(flags.INSTANCES_FORMAT)
    # TODO(b/36472296): Add a --uri flag test to kill a mutant.
    parser.display_info.AddUriFunc(_GetUriFromResource)

  def GetSqlClient(self):
    return api_util.SqlClient(api_util.API_VERSION_FALLBACK)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class ListBeta(_BaseList, base.ListCommand):
  """Lists Cloud SQL instances in a given project.

  Lists Cloud SQL instances in a given project in the alphabetical
  order of the instance name.
  """

  @staticmethod
  def Args(parser):
    parser.display_info.AddFormat(flags.INSTANCES_FORMAT_BETA)
    parser.display_info.AddUriFunc(_GetUriFromResourceBeta)

  def GetSqlClient(self):
    return api_util.SqlClient(api_util.API_VERSION_DEFAULT)
