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
"""Delete images command."""

from containerregistry.client import docker_name
from containerregistry.client.v2_2 import docker_http
from containerregistry.client.v2_2 import docker_session
from googlecloudsdk.api_lib.container.images import util
from googlecloudsdk.calliope import base
from googlecloudsdk.core import exceptions
from googlecloudsdk.core import http
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.resource import resource_printer


class Delete(base.DeleteCommand):
  """Delete existing images.

  The container images delete command of gcloud deletes a specified
  image and tags in a specified repository. Repositories
  must be hosted by the Google Container Registry.
  """

  detailed_help = {
      'DESCRIPTION':
          """\
          The container images delete command deletes the specified image from
          the registry. All associated tags are also deleted.
      """,
      'EXAMPLES':
          """\
          Deletes the image (and tags) from the input IMAGE_NAME:

            $ {command} <IMAGE_NAME>

      """,
  }

  def Collection(self):
    return 'container.images'

  @staticmethod
  def Args(parser):
    """Register flags for this command.

    Args:
      parser: An argparse.ArgumentParser-like object. It is mocked out in order
          to capture some information, but behaves like an ArgumentParser.
    """
    parser.add_argument(
        'image_names',
        nargs='+',
        help=('The IMAGE_NAME or IMAGE_NAMES to delete\n'
              'Format For Digest: *.gcr.io/repository@sha256:<digest> '
              'Format For Tag: *.gcr.io/repository:<tag>'))

    parser.add_argument(
        '--resolve-tag-to-digest',
        action='store_true',
        default=False,
        help=('Allows for images to be specified for deletion by tag. '
              'To remove a tag, please use the `untag` command.'))

    parser.add_argument(
        '--force-delete-tags',
        action='store_true',
        default=False,
        help=(
            'If there are tags pointing to an image to be deleted then they '
            'must all be specified explicitly, or this flag must be specified, '
            'for the command to succeed.'))

  def Run(self, args):
    """This is what ts called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Raises:
      InvalidImageNameError: If the user specified an invalid image name.
    Returns:
      A list of the deleted docker_name.Tag and docker_name.Digest objects
    """
    # IMAGE_NAME: The fully-qualified image name to delete (with a digest).
    # Deletes the layers. Ex. gcr.io/google-appengine/java(@DIGEST|:TAG).

    http_obj = http.Http()
    # collect input/validate
    digests, explicit_tags = self._ProcessImageNames(args.image_names)

    if explicit_tags and not args.resolve_tag_to_digest:
      raise exceptions.Error(
          'Referencing an image by tag will now delete the entire underlying '
          'image, as well as all associated tags. For the remainder of beta, '
          'please specify --resolve-tag-to-digest when deleting an image by '
          'tag. This will become the default behavior when `container images` '
          'leaves beta.')

    # Resolve tags to digests.
    for tag in explicit_tags:
      digests.add(util.GetDigestFromName(str(tag)))

    # Find all the tags that reference digests to be deleted.
    all_tags = set()
    for digest in digests:
      all_tags.update(util.GetDockerTagsForDigest(digest, http_obj))

    # Find all the tags that weren't specified explicitly.
    implicit_tags = all_tags.difference(explicit_tags)

    if implicit_tags and not args.force_delete_tags:
      log.error('Tags:')
      for tag in explicit_tags:
        log.error('- ' + str(tag))
      raise exceptions.Error(
          'This operation will implicitly delete the tags listed above. '
          'Please manually remove with the `untag` command or re-run with '
          '--force-delete-tags to confirm.')

    # Print the digests to be deleted.
    if digests:
      log.status.Print('Digests:')
    for digest in digests:
      self._PrintDigest(digest, http_obj)

    # Print the tags to be deleted.
    if explicit_tags:
      log.status.Print('Tags:')
    for tag in explicit_tags:
      log.status.Print('- ' + str(tag))

    # Prompt the user for consent to delete all the above.
    console_io.PromptContinue(
        'This operation will delete the tags and images identified by the '
        'digests above.',
        default=True,
        cancel_on_no=True)

    # The user has given explicit consent, merge the tags.
    explicit_tags.update(implicit_tags)

    # delete and collect output
    result = []
    for tag in explicit_tags:  # tags must be deleted before digests
      self._DeleteDockerTagOrDigest(tag, http_obj)
      result.append({'name': str(tag)})
    for digest in digests:
      self._DeleteDockerTagOrDigest(digest, http_obj)
      result.append({'name': str(digest)})
    return result

  def _ProcessImageNames(self, image_names):
    digests = set()
    tags = set()
    for image_name in image_names:
      docker_obj = util.GetDockerImageFromTagOrDigest(image_name)
      if isinstance(docker_obj, docker_name.Digest):
        digests.add(docker_obj)
      elif isinstance(docker_obj, docker_name.Tag):
        tags.add(docker_obj)
    return [digests, tags]

  def _MapDeleteErr(self, err, tag_or_digest):
    return util.GcloudifyRecoverableV2Errors(err, {
        403: 'Delete failed, access denied: {0}'.format(tag_or_digest),
        404: 'Delete failed, image not found: {0}'.format(tag_or_digest)
    })

  def _DeleteDockerTagOrDigest(self, tag_or_digest, http_obj):
    try:
      docker_session.Delete(
          creds=util.CredentialProvider(),
          name=tag_or_digest,
          transport=http_obj)
      log.DeletedResource(tag_or_digest)
    except docker_http.V2DiagnosticException as err:
      raise self._MapDeleteErr(err, tag_or_digest)

  def _DeleteDigestAndAssociatedTags(self, digest, http_obj):
    # Digest must not have any tags in order to be deleted.
    # Errors raised from tag deletion are deliberately uncaught.
    util.DeleteTagsFromDigest(digest, http_obj)
    tag_list = util.GetTagNamesForDigest(digest, http_obj)
    for tag in tag_list:
      log.DeletedResource(tag)

    try:
      docker_session.Delete(
          creds=util.CredentialProvider(), name=digest, transport=http_obj)
      log.DeletedResource(digest)
    except docker_http.V2DiagnosticException as err:
      raise self._MapDeleteErr(err, digest)

  def _PrintDigest(self, digest, http_obj):
    log.status.Print('- ' + str(digest))
    self._DisplayDigestTags(digest, http_obj)

  def _DisplayDigestTags(self, digest, http_obj):
    tag_list = util.GetTagNamesForDigest(digest, http_obj)
    if not tag_list:  # no tags on this digest, skip delete prompt
      return
    fmt = ('list[title="  Associated tags:"]')
    resource_printer.Print(tag_list, fmt, out=log.status)
