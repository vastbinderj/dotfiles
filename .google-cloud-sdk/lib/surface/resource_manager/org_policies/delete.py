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
"""Command to delete an OrgPolicy."""

from googlecloudsdk.api_lib.resource_manager import org_policies
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.resource_manager import org_policies_base
from googlecloudsdk.command_lib.resource_manager import org_policies_flags as flags
from googlecloudsdk.core import log


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class DeletePolicy(base.DeleteCommand):
  """Delete an OrgPolicy.

  Deletes an OrgPolicy associated with the specified resource.

  ## EXAMPLES

  The following command clears an OrgPolicy for constraint
  `serviceuser.services` on project `foo-project`:

    $ {command} serviceuser.services --project=foo-project
  """

  @staticmethod
  def Args(parser):
    flags.AddIdArgToParser(parser)
    flags.AddResourceFlagsToParser(parser)

  def Run(self, args):
    flags.CheckResourceFlags(args)
    service = org_policies_base.OrgPoliciesService(args)

    result = service.ClearOrgPolicy(self.ClearOrgPolicyRequest(args))
    log.DeletedResource(result)

  @staticmethod
  def ClearOrgPolicyRequest(args):
    messages = org_policies.OrgPoliciesMessages()
    resource_id = org_policies_base.GetResource(args)
    request = messages.ClearOrgPolicyRequest(
        constraint=org_policies.FormatConstraint(args.id))

    if args.project:
      return messages.CloudresourcemanagerProjectsClearOrgPolicyRequest(
          projectsId=resource_id, clearOrgPolicyRequest=request)
    elif args.organization:
      return messages.CloudresourcemanagerOrganizationsClearOrgPolicyRequest(
          organizationsId=resource_id, clearOrgPolicyRequest=request)
    return None
