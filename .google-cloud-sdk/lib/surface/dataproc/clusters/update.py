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

"""Update cluster command."""

from googlecloudsdk.api_lib.dataproc import exceptions
from googlecloudsdk.api_lib.dataproc import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.util import labels_util
from googlecloudsdk.core import log


class Update(base.UpdateCommand):
  """Update labels and/or the number of worker nodes in a cluster.

  Update the number of worker nodes and/or the labels in a cluster.

  ## EXAMPLES

  To resize a cluster, run:

    $ {command} my_cluster --num-workers 5

  To change the number preemptible workers in a cluster, run:

    $ {command} my_cluster --num-preemptible-workers 5

  To add the label 'customer=acme' to a cluster, run:

    $ {command} my_cluster --update-labels=customer=acme

  To update the label 'customer=ackme' to 'customer=acme', run:

    $ {command} my_cluster --update-labels=customer=acme

  To remove the label whose key is 'customer', run:

    $ {command} my_cluster --remove-labels=customer

  """

  @staticmethod
  def Args(parser):
    base.ASYNC_FLAG.AddToParser(parser)
    # Allow the user to specify new labels as well as update/remove existing
    labels_util.AddUpdateLabelsFlags(parser)
    parser.add_argument(
        'name',
        help='The name of the cluster to update.')
    parser.add_argument(
        '--num-workers',
        type=int,
        help='The new number of worker nodes in the cluster.')
    parser.add_argument(
        '--num-preemptible-workers',
        type=int,
        help='The new number of preemptible worker nodes in the cluster.')

  def Run(self, args):
    client = self.context['dataproc_client']
    messages = self.context['dataproc_messages']

    cluster_ref = util.ParseCluster(args.name, self.context)

    cluster_config = messages.ClusterConfig()
    changed_fields = []

    has_changes = False

    if args.num_workers is not None:
      worker_config = messages.InstanceGroupConfig(
          numInstances=args.num_workers)
      cluster_config.workerConfig = worker_config
      changed_fields.append('config.worker_config.num_instances')
      has_changes = True

    if args.num_preemptible_workers is not None:
      worker_config = messages.InstanceGroupConfig(
          numInstances=args.num_preemptible_workers)
      cluster_config.secondaryWorkerConfig = worker_config
      changed_fields.append(
          'config.secondary_worker_config.num_instances')
      has_changes = True

    # Update labels if the user requested it
    labels = None
    if args.update_labels or args.remove_labels:
      has_changes = True
      changed_fields.append('labels')

      # We need to fetch cluster first so we know what the labels look like. The
      # labels_util.UpdateLabels will fill out the proto for us with all the
      # updates and removals, but first we need to provide the current state
      # of the labels
      get_cluster_request = (
          client.MESSAGES_MODULE.DataprocProjectsRegionsClustersGetRequest(
              projectId=cluster_ref.projectId,
              region=cluster_ref.region,
              clusterName=cluster_ref.clusterName))
      current_cluster = client.projects_regions_clusters.Get(
          get_cluster_request)
      labels = labels_util.UpdateLabels(
          current_cluster.labels,
          messages.Cluster.LabelsValue,
          args.update_labels,
          args.remove_labels)

    if not has_changes:
      raise exceptions.ArgumentError(
          'Must specify at least one cluster parameter to update.')

    cluster = messages.Cluster(
        config=cluster_config,
        clusterName=cluster_ref.clusterName,
        labels=labels,
        projectId=cluster_ref.projectId)

    request = messages.DataprocProjectsRegionsClustersPatchRequest(
        clusterName=cluster_ref.clusterName,
        region=cluster_ref.region,
        projectId=cluster_ref.projectId,
        cluster=cluster,
        updateMask=','.join(changed_fields))

    operation = client.projects_regions_clusters.Patch(request)

    if args.async:
      log.status.write(
          'Updating [{0}] with operation [{1}].'.format(
              cluster_ref, operation.name))
      return

    util.WaitForOperation(
        operation,
        self.context,
        message='Waiting for cluster update operation',
        timeout_s=3600 * 3)

    request = client.MESSAGES_MODULE.DataprocProjectsRegionsClustersGetRequest(
        projectId=cluster_ref.projectId,
        region=cluster_ref.region,
        clusterName=cluster_ref.clusterName)
    cluster = client.projects_regions_clusters.Get(request)
    log.UpdatedResource(cluster_ref)
    return cluster
