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

"""'type-providers describe' command."""

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.deployment_manager import dm_beta_base
from googlecloudsdk.command_lib.deployment_manager import type_providers
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class Describe(base.DescribeCommand):
  """Describe a type provider entry in Type Registry."""

  detailed_help = {
      'EXAMPLES': """\
          To display information about a type provider, run:

            $ {command} NAME
          """,
  }

  @staticmethod
  def Args(parser):
    """Called by calliope to gather arguments for this command.

    Args:
      parser: argparse parser for specifying command line arguments
    """
    type_providers.AddTypeProviderNameFlag(parser)

  def Run(self, args):
    """Runs 'type-proivders describe'.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      The requested TypeProvider.

    Raises:
      HttpException: An http error response was received while executing the api
          request.
      InvalidArgumentException: The requested type provider could not be found.
    """
    type_provider_ref = dm_beta_base.GetResources().Parse(
        args.provider_name,
        params={'project': properties.VALUES.core.project.GetOrFail},
        collection='deploymentmanager.typeProviders')

    messages = dm_beta_base.GetMessages()
    request = messages.DeploymentmanagerTypeProvidersGetRequest(
        **type_provider_ref.AsDict())
    client = dm_beta_base.GetClient()
    return client.typeProviders.Get(request)

