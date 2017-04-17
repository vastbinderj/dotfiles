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

"""service-management operations describe command."""

import sys

from googlecloudsdk.api_lib.service_management import services_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.service_management import arg_parsers
from googlecloudsdk.command_lib.service_management import common_flags
from googlecloudsdk.core import log


_DETAILED_HELP = {
    'DESCRIPTION': """\
        This command will return information about an operation given the name
        of that operation.

        The amount of information inside an operation can be very large, so by
        default, only a summary is returned. If you want the entire operation
        resource, you can include the `--full` flag.

        Note that the `operations/` prefix of the operation name is optional
        and may be omitted.
        """,
    'EXAMPLES': """\
        To describe an operation resource named
        `operations/serviceConfigs.my-service.1`, run:

          $ {command} serviceConfigs.my-service.1

        To get the full operation resource, run:

          $ {command} serviceConfigs.my-service.1 --full
        """,
}

MAX_RESPONSE_BYTES = 1000


class Describe(base.DescribeCommand):
  """Describes an operation resource for a given operation name."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    common_flags.operation_flag(suffix='to describe').AddToParser(parser)

    parser.add_argument(
        '--full',
        action='store_true',
        default=False,
        help=('Print the entire operation resource, which could be large. '
              'By default, a summary will be printed instead.'))

  def Run(self, args):
    """Run 'service-management operations describe'.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      The response from the operations.Get API call.
    """
    messages = services_util.GetMessagesModule()
    client = services_util.GetClientInstance()

    operation_id = arg_parsers.GetOperationIdFromArg(args.operation)

    request = messages.ServicemanagementOperationsGetRequest(
        operationsId=operation_id,)

    operation = client.operations.Get(request)

    if (sys.getsizeof(str(operation.response)) > MAX_RESPONSE_BYTES and
        not args.full):
      log.warn('Response portion of operation resource redacted. '
               'Use --full to see the whole Operation.\n')
      operation.response = None

    # Set async to True because we don't need to wait for the operation
    # to complete to check the status of it.
    return services_util.GetProcessedOperationResult(operation, async=True)


Describe.detailed_help = _DETAILED_HELP
