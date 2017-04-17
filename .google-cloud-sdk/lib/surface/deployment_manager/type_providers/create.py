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

"""type-providers create command."""

from googlecloudsdk.api_lib.deployment_manager import dm_labels
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.deployment_manager import dm_beta_base
from googlecloudsdk.command_lib.deployment_manager import dm_write
from googlecloudsdk.command_lib.deployment_manager import flags
from googlecloudsdk.command_lib.deployment_manager import type_providers
from googlecloudsdk.command_lib.util import labels_util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties


def LogResource(request, async):
  log.CreatedResource(request.typeProvider.name,
                      kind='type_provider',
                      async=async)


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class Create(base.CreateCommand):
  """Create a type provider.

  This command inserts (creates) a new type provider based on a provided
  configuration file.
  """

  detailed_help = {
      'EXAMPLES': """\
          To create a new type provider, run:

            $ {command} my-type-provider --api-options-file=my-options.yaml --descriptor-url <descriptor URL> --description "My type."
          """,
  }

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    flags.AddAsyncFlag(parser)
    type_providers.AddTypeProviderNameFlag(parser)
    type_providers.AddApiOptionsFileFlag(parser)
    type_providers.AddDescriptionFlag(parser)
    type_providers.AddDescriptorUrlFlag(parser)
    labels_util.AddCreateLabelsFlags(parser)

  def Run(self, args):
    """Run 'type-providers create'.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Raises:
      HttpException: An http error response was received while executing api
          request.
    """
    messages = dm_beta_base.GetMessages()
    type_provider_ref = dm_beta_base.GetResources().Parse(
        args.provider_name,
        params={'project': properties.VALUES.core.project.GetOrFail},
        collection='deploymentmanager.typeProviders')
    update_labels_dict = labels_util.GetUpdateLabelsDictFromArgs(args)
    labels = dm_labels.UpdateLabels([],
                                    messages.TypeProviderLabelEntry,
                                    update_labels=update_labels_dict)

    type_provider = messages.TypeProvider(
        name=type_provider_ref.typeProvider,
        description=args.description,
        descriptorUrl=args.descriptor_url,
        labels=labels)

    type_providers.AddOptions(args.api_options_file, type_provider)
    request = messages.DeploymentmanagerTypeProvidersInsertRequest(
        project=type_provider_ref.project,
        typeProvider=type_provider)

    dm_write.Execute(request,
                     args.async,
                     dm_beta_base.GetClient().typeProviders.Insert,
                     LogResource)
