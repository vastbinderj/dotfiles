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

"""Base functions for DM write commands."""

import StringIO
import time

from googlecloudsdk.api_lib.deployment_manager import exceptions
from googlecloudsdk.command_lib.deployment_manager import dm_base
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import progress_tracker
from googlecloudsdk.core.resource import resource_printer


def Execute(request, async, call, logger):
  """Executes the request, managing asynchronous behavior.

  Args:
    request: The request to pass call.
    async: False if this call should poll for the Operation's success.
    call: Function that calls the appropriate API.
    logger: The log function to use for the operation. Should take the request
        and a boolean arg for async.

  Returns:
    The API response, probably an operation.

  Raises:
    HttpException: An http error response was received while executing api
        request.
    ToolException: Call encountered an error.
  """
  response = call(request)
  if not async:
    operation_ref = dm_base.GetResources().Parse(
        response.name,
        params={'project': properties.VALUES.core.project.GetOrFail},
        collection='deploymentmanager.operations')
    WaitForOperation(operation_ref.operation, response.operationType,
                     project=request.project)

  logger(request, async)
  if async:
    log.Print('Operation [{0}] running....'.format(response.name))

  return response


def GetOperationError(error):
  """Returns a ready-to-print string representation from the operation error.

  Args:
    error: operation error object

  Returns:
    A ready-to-print string representation of the error.
  """
  error_message = StringIO.StringIO()
  resource_printer.Print(error, 'yaml', out=error_message)
  return error_message.getvalue()


def WaitForOperation(operation_name, operation_description=None,
                     project=None, timeout=180):
  """Wait for an operation to complete.

  Polls the operation requested approximately every second, showing a
  progress indicator. Returns when the operation has completed.

  Args:
    operation_name: The name of the operation to wait on, as returned by
        operations.list.
    operation_description: A short description of the operation to wait on,
        such as 'create' or 'delete'. Will be displayed to the user.
    project: The name of the project that this operation belongs to.
    timeout: Number of seconds to wait for. Defaults to 3 minutes.

  Raises:
      HttpException: A http error response was received while executing api
          request. Will be raised if the operation cannot be found.
      OperationError: The operation finished with error(s).
      Error: The operation the timeout without completing.
  """
  tick_increment = 1  # every second(s)
  ticks = 0
  message = ('Waiting for {0}[{1}]'.format(
      operation_description + ' ' if operation_description else '',
      operation_name))
  request = dm_base.GetMessages().DeploymentmanagerOperationsGetRequest(
      project=project, operation=operation_name)
  with progress_tracker.ProgressTracker(message, autotick=False) as ticker:
    while ticks < timeout:
      operation = dm_base.GetClient().operations.Get(request)
      # Operation status is one of PENDING, RUNNING, DONE
      if operation.status == 'DONE':
        if operation.error:
          raise exceptions.OperationError(
              'Error in Operation [{0}]: {1}'.format(
                  operation_name, GetOperationError(operation.error)))
        else:  # Operation succeeded
          return

      ticks += tick_increment
      ticker.Tick()
      time.sleep(tick_increment)

    # Timeout exceeded
    raise exceptions.Error(
        'Wait for Operation [{0}] exceeded timeout [{1}].'.format(
            operation_name, str(timeout)))

