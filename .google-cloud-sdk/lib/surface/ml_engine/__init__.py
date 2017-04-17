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
"""Command group for ml-engine."""

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ml import flags
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resolvers
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class MlEngineBeta(base.Group):
  """Manage Cloud ML Engine jobs and models.

  The {command} command group lets you manage Google Cloud ML Engine jobs and
  training models.

  Cloud ML Engine is a managed service that enables you to easily build machine
  learning models, that work on any type of data, of any size. Create your model
  with the powerful TensorFlow framework that powers many Google products, from
  Google Photos to Google Cloud Speech.

  More information on Cloud ML Engine can be found here:
  https://cloud.google.com/ml
  and detailed documentation can be found here:
  https://cloud.google.com/ml/docs/
  """

  def __init__(self):
    project = properties.VALUES.core.project
    resolver = resolvers.FromProperty(project)
    resources.REGISTRY.SetParamDefault(
        'ml', collection=None, param='projectsId', resolver=resolver)
    resources.REGISTRY.RegisterApiByName('ml', 'v1beta1')
    # TODO(b/36712515) Remove this warning and cut over.
    log.warning(flags.V1BETA1_DEPRECATION_WARNING)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class MlEngineGa(base.Group):
  """Cloud ML Engine command groups."""

  def __init__(self):
    project = properties.VALUES.core.project
    resolver = resolvers.FromProperty(project)
    resources.REGISTRY.SetParamDefault(
        'ml', collection=None, param='projectsId', resolver=resolver)
    resources.REGISTRY.RegisterApiByName('ml', 'v1')
