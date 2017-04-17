# Copyright 2015 Google Inc. All Rights Reserved.
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

"""List project repositories."""

from googlecloudsdk.api_lib.sourcerepo import sourcerepo
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core import resolvers
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class List(base.ListCommand):
  """Lists all repositories in a particular project.

  By default, repos in the current project are listed; this can be overridden
  with the gcloud --project flag.
  """

  @staticmethod
  def Args(parser):
    base.URI_FLAG.RemoveFromParser(parser)
    # Here's some sample output (with the URL cut short)
    # REPO_NAME                     PROJECT_ID     SIZE      URL
    # ANewRepo                      kris-csr-test  0         https://...
    #
    # The resource name looks like projects/<projectid>/repos/reponame
    # We extract the project name as segment 1 and the repo name as segment 3
    # This will need to be modified when we allow repo names with slashes
    # to be listed via this interface.
    parser.display_info.AddFormat("""
          table(
            name.segment(3):label=REPO_NAME,
            name.segment(1):label=PROJECT_ID,
            size.yesno(no=0),
            firstof(mirror_config.url, url):label=URL
          )
        """)

  def Run(self, args):
    """Run the list command."""
    project_id = resolvers.FromProperty(properties.VALUES.core.project)
    res = resources.REGISTRY.Parse(
        None,
        params={'projectsId': project_id},
        collection='sourcerepo.projects')
    source_handler = sourcerepo.Source()
    return source_handler.ListRepos(res)
