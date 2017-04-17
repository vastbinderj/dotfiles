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
"""ml-engine jobs describe command."""

from googlecloudsdk.api_lib.ml import jobs
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ml import flags
from googlecloudsdk.command_lib.ml import jobs_util


def _AddDescribeArgs(parser):
  flags.JOB_NAME.AddToParser(parser)


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class DescribeBeta(base.DescribeCommand):
  """Describe a Cloud ML Engine job."""

  @staticmethod
  def Args(parser):
    _AddDescribeArgs(parser)

  def Run(self, args):
    job = jobs_util.Describe(jobs.JobsClient('v1beta1'), args.job)
    self.job = job  # Hack to make the Epilog method work
    return job

  def Epilog(self, resources_were_displayed):
    if resources_were_displayed:
      jobs_util.PrintDescribeFollowUp(self.job.jobId)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class DescribeGa(base.DescribeCommand):
  """Describe a Cloud ML Engine job."""

  @staticmethod
  def Args(parser):
    _AddDescribeArgs(parser)

  def Run(self, args):
    job = jobs_util.Describe(jobs.JobsClient('v1'), args.job)
    self.job = job  # Hack to make the Epilog method work
    return job

  def Epilog(self, resources_were_displayed):
    if resources_were_displayed:
      jobs_util.PrintDescribeFollowUp(self.job.jobId)
