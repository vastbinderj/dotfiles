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
"""Gets the IAM policy for the repository.
"""

import textwrap

from googlecloudsdk.api_lib.sourcerepo import sourcerepo
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core import resolvers
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class GetIamPolicy(base.DescribeCommand):
  """Get the IAM policy for the named repository."""

  detailed_help = {
      'DESCRIPTION':
          """\
          This command gets the IAM policy for the given repository.
      """,
      'EXAMPLES':
          textwrap.dedent("""\
          To get the IAM policy, issue the following command:\n
            $ gcloud beta source repos get-iam-policy REPO_NAME
      """),
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'name', metavar='REPOSITORY_NAME', help=('Name of the repository.'))

  def Run(self, args):
    """Gets the IAM policy for the repository.

    Args:
      args: argparse.Namespace, the arguments this command is run with.

    Returns:
      (sourcerepo_v1_messages.Policy) The IAM policy.

    Raises:
      ToolException: on project initialization errors.
    """
    project_id = resolvers.FromProperty(properties.VALUES.core.project)
    res = resources.REGISTRY.Parse(
        args.name,
        params={'projectsId': project_id},
        collection='sourcerepo.projects.repos')
    source = sourcerepo.Source()
    return source.GetIamPolicy(res)
