# Copyright 2014 Google Inc. All Rights Reserved.
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
"""Command for snapshotting disks."""

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import csek_utils
from googlecloudsdk.api_lib.compute import name_generator
from googlecloudsdk.api_lib.compute.operations import poller
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.compute import flags
from googlecloudsdk.command_lib.compute.disks import flags as disks_flags
from googlecloudsdk.core import exceptions as core_exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core import properties


DETAILED_HELP = {
    'DESCRIPTION': """\
        Create snapshots of Google Compute Engine persistent disks.

        *{command}* creates snapshots of persistent disks. Snapshots are useful
        for backing up data or copying a persistent disk. Once created,
        snapshots may be managed (listed, deleted, etc.) via
        ``gcloud compute snapshots''.
        """
}


def _CommonArgs(parser):
  """Add parser arguments common to all tracks."""
  SnapshotDisks.disks_arg.AddArgument(parser)

  parser.add_argument(
      '--description',
      help=('An optional, textual description for the snapshots being '
            'created.'))
  parser.add_argument(
      '--snapshot-names',
      type=arg_parsers.ArgList(min_length=1),
      metavar='SNAPSHOT_NAME',
      help="""\
      Names to assign to the snapshots. Without this option, the
      name of each snapshot will be a random, 16-character
      hexadecimal number that starts with a letter. The values of
      this option run parallel to the disks specified. For example,

        $ {command} my-disk-1 my-disk-2 my-disk-3 --snapshot-names snapshot-1,snapshot-2,snapshot-3

      will result in ``my-disk-1'' being snapshotted as
      ``snapshot-1'', ``my-disk-2'' as ``snapshot-2'', and so on.
      """)
  parser.add_argument(
      '--guest-flush',
      action='store_true',
      default=False,
      help=('Create an application consistent snapshot by informing the OS '
            'to prepare for the snapshot process. Currently only supported '
            'on Windows instances using the Volume Shadow Copy Service '
            '(VSS).'))
  csek_utils.AddCsekKeyArgs(parser, flags_about_creation=False)

  base.ASYNC_FLAG.AddToParser(parser)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class SnapshotDisks(base.SilentCommand):
  """Create snapshots of Google Compute Engine persistent disks."""

  @staticmethod
  def Args(parser):
    SnapshotDisks.disks_arg = disks_flags.MakeDiskArg(plural=True)
    _CommonArgs(parser)

  def Run(self, args):
    """Returns a list of requests necessary for snapshotting disks."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())

    disk_refs = SnapshotDisks.disks_arg.ResolveAsResource(
        args, holder.resources,
        scope_lister=flags.GetDefaultScopeLister(holder.client))
    if args.snapshot_names:
      if len(disk_refs) != len(args.snapshot_names):
        raise exceptions.ToolException(
            '[--snapshot-names] must have the same number of values as disks '
            'being snapshotted.')
      snapshot_names = args.snapshot_names
    else:
      # Generates names like "d52jsqy3db4q".
      snapshot_names = [name_generator.GenerateRandomName()
                        for _ in disk_refs]

    snapshot_refs = [
        holder.resources.Parse(
            snapshot_name,
            params={
                'project': properties.VALUES.core.project.GetOrFail,
            },
            collection='compute.snapshots')
        for snapshot_name in snapshot_names]

    client = holder.client.apitools_client
    messages = holder.client.messages

    requests = []

    for disk_ref, snapshot_ref in zip(disk_refs, snapshot_refs):
      # This feature is only exposed in alpha/beta
      allow_rsa_encrypted = self.ReleaseTrack() in [base.ReleaseTrack.ALPHA,
                                                    base.ReleaseTrack.BETA]
      csek_keys = csek_utils.CsekKeyStore.FromArgs(args, allow_rsa_encrypted)
      disk_key_or_none = csek_utils.MaybeLookupKeyMessage(
          csek_keys, disk_ref, client)

      # TODO(b/35852475) drop test after 'guestFlush' goes GA.
      if hasattr(args, 'guest_flush') and args.guest_flush:
        request_kwargs = {'guestFlush': True}
      else:
        request_kwargs = {}

      if disk_ref.Collection() == 'compute.disks':
        request = messages.ComputeDisksCreateSnapshotRequest(
            disk=disk_ref.Name(),
            snapshot=messages.Snapshot(
                name=snapshot_ref.Name(),
                description=args.description,
                sourceDiskEncryptionKey=disk_key_or_none
            ),
            project=disk_ref.project,
            zone=disk_ref.zone,
            **request_kwargs)
        requests.append((client.disks, 'CreateSnapshot', request))
      elif disk_ref.Collection() == 'compute.regionDisks':
        request = messages.ComputeRegionDisksCreateSnapshotRequest(
            disk=disk_ref.Name(),
            snapshot=messages.Snapshot(
                name=snapshot_ref.Name(),
                description=args.description,
                sourceDiskEncryptionKey=disk_key_or_none
            ),
            project=disk_ref.project,
            region=disk_ref.region,
            **request_kwargs)
        requests.append((client.regionDisks, 'CreateSnapshot', request))

    errors_to_collect = []
    responses = holder.client.BatchRequests(requests, errors_to_collect)
    for r in responses:
      err = getattr(r, 'error', None)
      if err:
        errors_to_collect.append(poller.OperationErrors(err.errors))
    if errors_to_collect:
      raise core_exceptions.MultiError(errors_to_collect)

    operation_refs = [holder.resources.Parse(r.selfLink) for r in responses]

    if args.async:
      for operation_ref in operation_refs:
        log.status.Print('Disk snapshot in progress for [{}].'
                         .format(operation_ref.SelfLink()))
      log.status.Print('Use [gcloud compute operations describe URI] command '
                       'to check the status of the operation(s).')
      return responses

    operation_poller = poller.BatchPoller(
        holder.client, client.snapshots, snapshot_refs)
    return waiter.WaitFor(
        operation_poller, poller.OperationBatch(operation_refs),
        'Creating snapshot(s) {0}'
        .format(', '.join(s.Name() for s in snapshot_refs)))


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class SnapshotDisksBeta(SnapshotDisks):
  """Create snapshots of Google Compute Engine persistent disks."""

  @staticmethod
  def Args(parser):
    SnapshotDisks.disks_arg = disks_flags.MakeDiskArg(plural=True)
    _CommonArgs(parser)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class SnapshotDisksAlpha(SnapshotDisks):
  """Create snapshots of Google Compute Engine persistent disks."""

  @staticmethod
  def Args(parser):
    SnapshotDisks.disks_arg = disks_flags.MakeDiskArgZonalOrRegional(
        plural=True)
    _CommonArgs(parser)


SnapshotDisks.detailed_help = DETAILED_HELP
SnapshotDisksBeta.detailed_help = DETAILED_HELP
