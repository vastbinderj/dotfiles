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

"""A command that searches the gcloud group and command tree."""

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.search_help import search
from googlecloudsdk.command_lib.search_help import table


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class HelpSearch(base.Command):
  """Search the help text of gcloud commands."""

  detailed_help = {
      'DESCRIPTION': """\
          Search the help text of gcloud commands for a term
          of interest. Prints the command name and a summary
          of the help text for any general release command whose
          help text contains the searched term."""}

  @staticmethod
  def Args(parser):
    parser.add_argument('term',
                        help=('Term to search for.'))

  def Run(self, args):
    table_path = table.IndexPath()
    return search.RunSearch(table_path, [args.term], self.cli)

  def Format(self, unused_args):
    return ("table(path.join(sep=' '):label='COMMAND', "
            "summary:wrap:label='HELP')")
