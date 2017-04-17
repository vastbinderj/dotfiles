#!/usr/bin/env python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""gcloud command line tool."""

import time
START_TIME = time.time()

# pylint:disable=g-bad-import-order
# pylint:disable=g-import-not-at-top, We want to get the start time first.
import errno
import os
import sys

from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import cli
from googlecloudsdk.command_lib import crash_handling
from googlecloudsdk.command_lib.ml import flags
from googlecloudsdk.core import config
from googlecloudsdk.core import log
from googlecloudsdk.core import metrics
from googlecloudsdk.core import properties
from googlecloudsdk.core.updater import local_state
from googlecloudsdk.core.updater import update_manager
from googlecloudsdk.core.util import keyboard_interrupt
from googlecloudsdk.core.util import platforms
import surface


# Disable stack traces when the command is interrupted.
keyboard_interrupt.InstallHandler()


def _DoStartupChecks():
  if not platforms.PythonVersion().IsCompatible():
    sys.exit(1)

_DoStartupChecks()

if not config.Paths().sdk_root:
  # Don't do update checks if there is no install root.
  properties.VALUES.component_manager.disable_update_check.Set(True)


def UpdateCheck(command_path, **unused_kwargs):
  try:
    update_manager.UpdateManager.PerformUpdateCheck(command_path=command_path)
  # pylint:disable=broad-except, We never want this to escape, ever. Only
  # messages printed should reach the user.
  except Exception:
    log.debug('Failed to perform update check.', exc_info=True)


def IssueMlWarning(command_path=None):
  del command_path  # Unused in _IssueMlWarning
  log.warn(
      'The `gcloud beta ml` commands have been renamed and will soon be '
      'removed. Please use `gcloud ml-engine` instead.')
  log.warn(flags.V1BETA1_DEPRECATION_WARNING)


def _IssueTestWarning(command_path=None):
  del command_path  # Unused in _IssueTestWarning
  log.warn(
      'The `gcloud beta test` commands have been renamed and will soon be '
      'removed. Please use `gcloud firebase test` instead.')


def CreateCLI(surfaces):
  """Generates the gcloud CLI from 'surface' folder with extra surfaces.

  Args:
    surfaces: list(tuple(dot_path, dir_path)), extra commands or subsurfaces
              to add, where dot_path is calliope command path and dir_path
              path to command group or command.
  Returns:
    calliope cli object.
  """
  def VersionFunc():
    generated_cli.Execute(['version'])

  pkg_root = os.path.dirname(os.path.dirname(surface.__file__))
  loader = cli.CLILoader(
      name='gcloud',
      command_root_directory=os.path.join(pkg_root, 'surface'),
      allow_non_existing_modules=True,
      version_func=VersionFunc)
  loader.AddReleaseTrack(base.ReleaseTrack.ALPHA,
                         os.path.join(pkg_root, 'surface', 'alpha'),
                         component='alpha')
  loader.AddReleaseTrack(base.ReleaseTrack.BETA,
                         os.path.join(pkg_root, 'surface', 'beta'),
                         component='beta')

  for dot_path, dir_path in surfaces:
    loader.AddModule(dot_path, dir_path, component=None)

  if os.path.exists(os.path.join(pkg_root, 'surface', 'beta')):
    for mod in ['jobs', 'local', 'models', 'operations', 'versions',
                'init_project.py', 'predict.py']:
      loader.AddModule(
          'beta.ml.{}'.format(mod.replace('.py', '')),
          os.path.join(pkg_root, 'surface', 'ml_engine', mod))
    loader.RegisterPreRunHook(IssueMlWarning,
                              include_commands=r'gcloud\.beta\.ml\..*',
                              exclude_commands=(
                                  r'gcloud\.beta\.ml\.vision\..*'
                                  r'|gcloud\.beta\.ml\.language\..*'
                                  r'|gcloud\.beta\.ml$'
                              ))

    # TODO(b/35758009): Remove cloned beta.test commands and PreRunHook after a
    # suitable deprecation period.
    # Clone 'firebase test' surface into 'beta test' for backward compatibility.
    loader.AddModule('beta.test',
                     os.path.join(pkg_root, 'surface', 'firebase', 'test'))
    # The above call to AddModule() hides the `beta test android devices` group,
    # so add it back.
    loader.AddModule(
        'beta.test.android.devices',
        os.path.join(pkg_root, 'surface', 'test', 'android', 'devices'))
    loader.RegisterPreRunHook(_IssueTestWarning,
                              include_commands=r'gcloud\.beta\.test\..*')

  # Check for updates on shutdown but not for any of the updater commands.
  loader.RegisterPostRunHook(UpdateCheck,
                             exclude_commands=r'gcloud\.components\..*')
  generated_cli = loader.Generate()
  return generated_cli


def main(gcloud_cli=None):
  metrics.Started(START_TIME)
  # TODO(b/36049857): Put a real version number here
  metrics.Executions(
      'gcloud',
      local_state.InstallationState.VersionForInstalledComponent('core'))
  if gcloud_cli is None:
    gcloud_cli = CreateCLI([])
  try:
    try:
      gcloud_cli.Execute()
    except IOError as err:
      # We want to ignore EPIPE IOErrors.
      # By default, Python ignores SIGPIPE (see
      # http://utcc.utoronto.ca/~cks/space/blog/python/SignalExceptionSurprise).
      # This means that attempting to write any output to a closed pipe (e.g. in
      # the case of output piped to `head` or `grep -q`) will result in an
      # IOError, which gets reported as a gcloud crash. We don't want this
      # behavior, so we ignore EPIPE (it's not a real error; it's a normal thing
      # to occur).
      # Before, we restore the SIGPIPE signal handler, but that caused issues
      # with scripts/programs that wrapped gcloud.
      if err.errno != errno.EPIPE:
        raise
  except Exception as err:  # pylint:disable=broad-except
    crash_handling.HandleGcloudCrash(err)
    if properties.VALUES.core.print_unhandled_tracebacks.GetBool():
      # We want to see the traceback as normally handled by Python
      raise
    else:
      # This is the case for most non-Cloud SDK developers. They shouldn't see
      # the full stack trace, but just the nice "gcloud crashed" message.
      sys.exit(1)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    keyboard_interrupt.HandleInterrupt()
