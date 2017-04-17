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

"""This package provides tools for saving docker images."""



import cStringIO
import gzip
import hashlib
import json
import tarfile

from containerregistry.client import docker_name
from containerregistry.client.v1 import save as v1_save
from containerregistry.client.v2 import v1_compat
from containerregistry.client.v2_2 import docker_image as v2_2_image
from containerregistry.client.v2_2 import v2_compat



def _diff_id(blob):
  compressed_file = cStringIO.StringIO(blob)
  decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')
  return 'sha256:' + hashlib.sha256(decompressed_file.read()).hexdigest()


def tarball(
    name,
    image,
    tar
):
  """Produce a "docker save" compatible tarball from the DockerImage.

  Args:
    name: The tag name to write into repositories and manifest.json
    image: a docker image to save.
    tar: the open tarfile into which we are writing the image tarball.
  """

  def add_file(filename, contents):
    info = tarfile.TarInfo(filename)
    info.size = len(contents)
    tar.addfile(tarinfo=info, fileobj=cStringIO.StringIO(contents))

  # The config file is stored in a blob file named with its digest.
  digest = hashlib.sha256(image.config_file()).hexdigest()
  add_file('./' + digest + '.json', image.config_file())

  # We don't just exclude the empty tar because we leave its diff_id
  # in the set when coming through v2_compat.V22FromV2
  cfg = json.loads(image.config_file())
  diffs = set(cfg.get('rootfs', {}).get('diff_ids', []))

  with v2_compat.V2FromV22(image) as v2_img:
    with v1_compat.V1FromV2(v2_img) as v1_img:
      # v2.2 tarballs are a superset of v1 tarballs, so delegate
      # to v1 to save itself.
      v1_save.tarball(name, v1_img, tar)

      # The manifest.json file contains a list of the images to load
      # and how to tag them.  Each entry consists of three fields:
      #  - Config: the name of the image's config_file() within the
      #           saved tarball.
      #  - Layers: the list of filenames for the blobs constituting
      #           this image.  The order is the reverse of the v1
      #           ancestry ordering.
      #  - RepoTags: the list of tags to apply to this image once it
      #             is loaded.
      add_file('./manifest.json', json.dumps([{
          'Config': digest + '.json',
          'Layers': [
              layer_id + '/layer.tar'
              for layer_id in reversed(v1_img.ancestry(v1_img.top()))
              if _diff_id(v1_img.layer(layer_id)) in diffs
          ],
          'RepoTags': [str(name)]
      }], sort_keys=True))
