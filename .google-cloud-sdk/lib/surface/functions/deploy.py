# Copyright 2015 Google Inc. All Rights Reserved.
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

"""'functions deploy' command."""
import httplib
import os
import random
import re
import string

from apitools.base.py import exceptions as apitools_exceptions

from googlecloudsdk.api_lib.compute import utils
from googlecloudsdk.api_lib.functions import cloud_storage as storage
from googlecloudsdk.api_lib.functions import exceptions
from googlecloudsdk.api_lib.functions import operations
from googlecloudsdk.api_lib.functions import util
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.functions.deploy import util as deploy_util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources
from googlecloudsdk.core.console import progress_tracker
from googlecloudsdk.core.util import archive
from googlecloudsdk.core.util import files as file_utils


def _FunctionArgs(parser):
  """Add arguments specyfying functions behavior to the parser."""
  parser.add_argument(
      'name', help='Intended name of the new function.',
      type=util.ValidateFunctionNameOrRaise)
  parser.add_argument(
      '--memory',
      type=arg_parsers.BinarySize(
          suggested_binary_size_scales=['KB', 'MB', 'MiB', 'GB', 'GiB'],
          default_unit='MB'),
      help="""\
      The amount of memory allocated to your function.

      Allowed values are: 128MB, 256MB, 512MB, 1024MB, and 2048MB. By default,
      256 MB is allocated to each function.""")
  parser.add_argument(
      '--timeout',
      help=('The function execution timeout, e.g. 30s for 30 seconds. '
            'Defaults to 60 seconds.'),
      type=arg_parsers.Duration(lower_bound='1s'))


def _SourceCodeArgs(parser):
  """Add arguments specyfying functions source code to the parser."""
  path_group = parser.add_mutually_exclusive_group()
  path_group.add_argument(
      '--local-path',
      help=('Path to local directory with source code. Required with '
            '--stage-bucket flag.'))
  path_group.add_argument(
      '--source-path',
      help=('Path to directory with source code in Cloud Source '
            'Repositories, when you specify this parameter --source-url flag '
            'is required.'))
  source_group = parser.add_mutually_exclusive_group()
  source_group.add_argument(
      '--stage-bucket',
      help=('Name of Google Cloud Storage bucket in which source code will '
            'be stored. Required if a function is deployed from a local '
            'directory.'),
      type=util.ValidateAndStandarizeBucketUriOrRaise)
  source_group.add_argument(
      '--source-url',
      help=('The Url of a remote repository that holds the function being '
            'deployed. It is of the form: '
            'https://source.developers.google.com/p/{project_id}/'
            'r/{repo_name}/, where you should substitute your data for '
            'values inside the curly brackets. You can omit "r/{repo_name}/" '
            'in which case the "default" repository is taken. '
            'One of the parameters --source-revision, --source-branch, '
            'or --source-tag can be given to specify the version in the '
            'repository. If none of them are provided, the last revision '
            'from the master branch is used. If this parameter is given, '
            'the parameter --source is required and describes the path '
            'inside the repository.'))
  source_version_group = parser.add_mutually_exclusive_group()
  source_version_group.add_argument(
      '--source-revision',
      help=('The revision ID (for instance, git commit hash) that will be '
            'used to get the source code of the function. Can be specified '
            'only together with --source-url parameter.'))
  source_version_group.add_argument(
      '--source-branch',
      help=('The branch that will be used to get the source code of the '
            'function.  The most recent revision on this branch will be '
            'used. Can be specified only together with --source-url '
            'parameter. If not specified defaults to `master`.'))
  source_version_group.add_argument(
      '--source-tag',
      help="""\
      The revision tag for the source that will be used as the source
      code of the function. Can be specified only together with
      --source-url parameter.""")
  parser.add_argument(
      '--entry-point',
      type=util.ValidateEntryPointNameOrRaise,
      help="""\
      By default when a Google Cloud Function is triggered, it executes a
      JavaScript function with the same name. Or, if it cannot find a
      function with the same name, it executes a function named `function`.
      You can use this flag to override the default behavior, by specifying
      the name of a JavaScript function that will be executed when the
      Google Cloud Function is triggered."""
  )
  parser.add_argument(
      '--include-ignored-files',
      help=('Deploy sources together with files which are normally ignored '
            '(contents of node_modules directory). This flag has an effect '
            'only if a function is deployed from a local directory.'),
      default=False,
      action='store_true')


def _TriggerArgs(parser):
  """Add arguments specyfying functions trigger to the parser."""
  trigger_group = parser.add_mutually_exclusive_group(required=True)
  trigger_group.add_argument(
      '--trigger-topic',
      help=('Name of Pub/Sub topic. Every message published in this topic '
            'will trigger function execution with message contents passed as '
            'input data.'),
      type=util.ValidatePubsubTopicNameOrRaise)
  trigger_group.add_argument(
      '--trigger-bucket',
      help=('Google Cloud Storage bucket name. Every change in files in this '
            'bucket will trigger function execution.'),
      type=util.ValidateAndStandarizeBucketUriOrRaise)
  trigger_group.add_argument(
      '--trigger-http', action='store_true',
      help="""\
      Function will be assigned an endpoint, which you can view by using
      the `describe` command. Any HTTP request (of a supported type) to the
      endpoint will trigger function execution. Supported HTTP request
      types are: POST, PUT, GET, DELETE, and OPTIONS.""")
  trigger_group.add_argument(
      '--trigger-provider',
      metavar='PROVIDER',
      choices=sorted(util.input_trigger_provider_registry.ProvidersLabels()),
      help=('Trigger this function in response to an event in another '
            'service. For a list of acceptable values, call `gcloud '
            'functions event-types list`.'),
      hidden=True,
      )
  trigger_provider_spec_group = parser.add_argument_group()
  # The validation performed by argparse is incomplete, as the set of valid
  # provider/event combinations is limited. This should be more thoroughly
  # validated at runtime.
  trigger_provider_spec_group.add_argument(
      '--trigger-event',
      metavar='EVENT_TYPE',
      choices=['topic.publish', 'object.change', 'user.create', 'user.delete',
               'data.write'],
      help=('Specifies which action should trigger the function. If omitted, '
            'a default EVENT_TYPE for --trigger-provider will be used. For a '
            'list of acceptable values, call functions event_types list.'),
      hidden=True,
  )
  # check later as type of applicable input depends on options above
  trigger_provider_spec_group.add_argument(
      '--trigger-resource',
      metavar='RESOURCE',
      help=('Specifies which resource from --trigger-provider is being '
            'observed. E.g. if --trigger-provider is cloud.storage, '
            '--trigger-resource must be a bucket name. For a list of '
            'expected resources, call functions event_types list.'),
      hidden=True,
  )


class Deploy(base.Command):
  """Creates a new function or updates an existing one."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    _FunctionArgs(parser)
    _SourceCodeArgs(parser)
    _TriggerArgs(parser)

  @util.CatchHTTPErrorRaiseHTTPException
  def _GetExistingFunction(self, name):
    client = self.context['functions_client']
    messages = self.context['functions_messages']
    try:
      # We got response for a get request so a function exists.
      return client.projects_locations_functions.Get(
          messages.CloudfunctionsProjectsLocationsFunctionsGetRequest(
              name=name))
    except apitools_exceptions.HttpError as error:
      if error.status_code == httplib.NOT_FOUND:
        # The function has not been found.
        return None
      raise

  def _GenerateRemoteZipFileName(self, args):
    sufix = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
    return '{0}-{1}-{2}.zip'.format(
        properties.VALUES.functions.region.Get(), args.name, sufix)

  def _UploadFile(self, source, target):
    return storage.Upload(source, target)

  def _CreateZipFile(self, tmp_dir, args):
    zip_file_name = os.path.join(tmp_dir, 'fun.zip')
    local_path = deploy_util.GetLocalPath(args)
    try:
      if args.include_ignored_files:
        archive.MakeZipFromDir(zip_file_name, local_path)
      else:
        log.info('Not including node_modules in deployed code. To include '
                 'node_modules in uploaded code use --include-ignored-files '
                 'flag.')
        archive.MakeZipFromDir(
            zip_file_name,
            local_path,
            skip_file_regex=r'(node_modules{}.*)|(node_modules)'.format(
                re.escape(os.sep)))
    except ValueError as e:
      raise exceptions.FunctionsError(
          'Error creating a ZIP archive with the source code '
          'for directory {0}: {1}'.format(local_path, str(e)))
    return zip_file_name

  def _EventTrigger(self, trigger_provider, trigger_event,
                    trigger_resource):
    messages = self.context['functions_messages']
    event_trigger = messages.EventTrigger()
    event_type_ref = resources.REGISTRY.Parse(
        None,
        params={
            'triggerProvider': trigger_provider,
            'triggerEvent': trigger_event
        },
        collection='cloudfunctions.providers.event_types'
    )
    event_trigger.eventType = event_type_ref.RelativeName()
    event_trigger.resource = (
        deploy_util.ConvertTriggerArgsToRelativeName(
            trigger_provider,
            trigger_event,
            trigger_resource))
    return event_trigger

  def _PrepareFunctionWithoutSources(
      self, name, entry_point, timeout_sec, trigger_http, trigger_params):
    """Creates a function object without filling in the sources properties.

    Args:
      name: str, name of the function (resource).
      entry_point: str, name of the function (in deployed code) to be executed.
      timeout_sec: int, maximum time allowed for function execution, in seconds.
      trigger_http: bool, indicates whether function should have a HTTPS
                    trigger; when truthy trigger_params argument is ignored.
      trigger_params: None or dict from str to str, the dict is assmed to
                      contain exactly the following keys: trigger_provider,
                      trigger_event, trigger_resource.

    Returns:
      The specified function with its description and configured filter.
    """
    messages = self.context['functions_messages']
    function = messages.CloudFunction()
    function.name = name
    if entry_point:
      function.entryPoint = entry_point
    if timeout_sec:
      function.timeout = str(timeout_sec) + 's'
    if trigger_http:
      function.httpsTrigger = messages.HTTPSTrigger()
    else:
      function.eventTrigger = self._EventTrigger(**trigger_params)
    return function

  def _DeployFunction(self, name, location, args, deploy_method,
                      trigger_params):
    function = self._PrepareFunctionWithoutSources(
        name, args.entry_point, args.timeout, args.trigger_http, trigger_params)
    if args.source_url:
      messages = self.context['functions_messages']
      source_path = args.source_path
      source_branch = args.source_branch or 'master'
      function.sourceRepository = messages.SourceRepository(
          tag=args.source_tag, branch=source_branch,
          revision=args.source_revision, repositoryUrl=args.source_url,
          sourcePath=source_path)
    else:
      function.sourceArchiveUrl = self._PrepareSourcesOnGcs(args)
    memory_mb = utils.BytesToMb(args.memory)
    if memory_mb:
      function.availableMemoryMb = memory_mb
    return deploy_method(location, function)

  def _PrepareSourcesOnGcs(self, args):
    remote_zip_file = self._GenerateRemoteZipFileName(args)
    gcs_url = storage.BuildRemoteDestination(args.stage_bucket, remote_zip_file)
    with file_utils.TemporaryDirectory() as tmp_dir:
      zip_file = self._CreateZipFile(tmp_dir, args)
      if self._UploadFile(zip_file, gcs_url) != 0:
        raise exceptions.FunctionsError(
            'Failed to upload the function source code to the bucket {0}'
            .format(args.stage_bucket))
    return gcs_url

  @util.CatchHTTPErrorRaiseHTTPException
  def _CreateFunction(self, location, function):
    client = self.context['functions_client']
    messages = self.context['functions_messages']
    op = client.projects_locations_functions.Create(
        messages.CloudfunctionsProjectsLocationsFunctionsCreateRequest(
            location=location, cloudFunction=function))
    with progress_tracker.ProgressTracker(
        'Deploying function (may take a while - up to 2 minutes)'):
      operations.Wait(op, messages, client)
    return self._GetExistingFunction(function.name)

  @util.CatchHTTPErrorRaiseHTTPException
  def _UpdateFunction(self, unused_location, function):
    client = self.context['functions_client']
    messages = self.context['functions_messages']
    op = client.projects_locations_functions.Update(function)
    with progress_tracker.ProgressTracker(
        'Deploying function (may take a while - up to 2 minutes)'):
      operations.Wait(op, messages, client)
    return self._GetExistingFunction(function.name)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The specified function with its description and configured filter.

    Raises:
      FunctionsError if command line parameters are not valid.
    """
    trigger_params = deploy_util.DeduceAndCheckArgs(args)
    project = properties.VALUES.core.project.Get(required=True)
    registry = self.context['registry']
    location_ref = registry.Parse(
        properties.VALUES.functions.region.Get(),
        params={'projectsId': project},
        collection='cloudfunctions.projects.locations')
    location = location_ref.RelativeName()
    function_ref = registry.Parse(
        args.name, params={
            'projectsId': project,
            'locationsId': properties.VALUES.functions.region.Get()},
        collection='cloudfunctions.projects.locations.functions')
    function_url = function_ref.RelativeName()

    function = self._GetExistingFunction(function_url)
    if function is None:
      return self._DeployFunction(function_url, location, args,
                                  self._CreateFunction, trigger_params)
    else:
      return self._DeployFunction(function_url, location, args,
                                  self._UpdateFunction, trigger_params)
