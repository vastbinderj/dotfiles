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
"""ml-engine models create command."""
from googlecloudsdk.api_lib.ml import models
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ml import flags
from googlecloudsdk.command_lib.ml import models_util


def _AddCreateArgs(parser):
  """Get arguments for the `ml-engine models create` command."""
  flags.GetModelName().AddToParser(parser)
  parser.add_argument(
      '--regions',
      metavar='REGION',
      type=arg_parsers.ArgList(min_length=1),
      help="""\
The Google Cloud region where the model will be deployed (currently only a
single region is supported).

Will soon be required, but defaults to 'us-central1' for now.
""")
  parser.add_argument(
      '--enable-logging',
      action='store_true',
      help=('If set, enables StackDriver Logging for online prediction.'))


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class CreateBeta(base.CreateCommand):
  """Create a new Cloud ML Engine model."""

  def Collection(self):
    return 'ml.models'

  @staticmethod
  def Args(parser):
    _AddCreateArgs(parser)

  def Run(self, args):
    models_util.Create(models.ModelsClient('v1beta1'), args.model,
                       regions=args.regions, enable_logging=args.enable_logging)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class CreateGa(base.CreateCommand):
  """Create a new Cloud ML Engine model."""

  def Collection(self):
    return 'ml.models'

  @staticmethod
  def Args(parser):
    _AddCreateArgs(parser)

  def Run(self, args):
    models_util.Create(models.ModelsClient('v1'), args.model,
                       regions=args.regions, enable_logging=args.enable_logging)
