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
import json
import tarfile

from containerregistry.client import docker_name
from containerregistry.client.v1 import docker_image



def tarball(
    name,
    image,
    tar
):
  """Produce a "docker save" compatible tarball from the DockerImage.

  Args:
    name: The tag name to write into the repositories file.
    image: a docker image to save.
    tar: the open tarfile into which we are writing the image tarball.
  """

  def add_file(filename, contents):
    info = tarfile.TarInfo(filename)
    info.size = len(contents)
    tar.addfile(tarinfo=info, fileobj=cStringIO.StringIO(contents))

  for layer_id in image.ancestry(image.top()):
    # Each layer is encoded as a directory in the larger tarball of the form:
    #  {layer_id}\
    #    layer.tar
    #    VERSION
    #    json

    # VERSION generally seems to contain 1.0, not entirely sure
    # what the point of this is.
    add_file('./' + layer_id + '/VERSION', '1.0')

    # Add the unzipped layer tarball
    buf = cStringIO.StringIO(image.layer(layer_id))
    f = gzip.GzipFile(mode='rb', fileobj=buf)
    add_file('./' + layer_id + '/layer.tar', f.read())

    # Now the json metadata
    add_file('./' + layer_id + '/json', image.json(layer_id))

  # Add the metadata tagging the top layer.
  add_file('./repositories', json.dumps({
      '{registry}/{repository}'.format(
          registry=name.registry,
          repository=name.repository): {
              name.tag: image.top()
          }
      }))

  # Add our convenience file with the top layer's ID.
  add_file('./top', image.top())
