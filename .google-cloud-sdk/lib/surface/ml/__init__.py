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
"""Command group for Machine Learning."""

from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core import resolvers
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class Ml(base.Group):
  """Use Google Cloud machine learning capabilities."""

  def __init__(self):
    # TODO(b/36565419): Remove
    project = properties.VALUES.core.project
    resolver = resolvers.FromProperty(project)
    resources.REGISTRY.SetParamDefault(
        'ml', collection=None, param='projectsId', resolver=resolver)
    resources.REGISTRY.RegisterApiByName('ml', 'v1beta1')
