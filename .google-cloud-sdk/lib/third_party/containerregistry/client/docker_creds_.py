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

"""This package exposes credentials for talking to a Docker registry."""



import abc
import base64
import json
import os
import subprocess

from containerregistry.client import docker_name
import httplib2  # pylint: disable=unused-import
from oauth2client import client as oauth2client  # pylint: disable=unused-import


class Provider(object):
  """Interface for providing User Credentials for use with a Docker Registry."""

  __metaclass__ = abc.ABCMeta  # For enforcing that methods are overriden.

  @abc.abstractmethod
  def Get(self):
    """Produces a value suitable for use in the Authorization header."""


class Anonymous(Provider):
  """Implementation for anonymous access."""

  def Get(self):
    """Implement anonymous authentication."""
    return ''


class SchemeProvider(Provider):
  """Implementation for providing a challenge response credential."""

  def __init__(self, scheme):
    self._scheme = scheme

  @property
  @abc.abstractmethod
  def suffix(self):
    """Returns the authentication payload to follow the auth scheme."""

  def Get(self):
    """Gets the credential in a form suitable for an Authorization header."""
    return '%s %s' % (self._scheme, self.suffix)


class Basic(SchemeProvider):
  """Implementation for providing a username/password-based creds."""

  def __init__(self, username, password):
    super(Basic, self).__init__('Basic')
    self._username = username
    self._password = password

  @property
  def username(self):
    return self._username

  @property
  def password(self):
    return self._password

  @property
  def suffix(self):
    return base64.b64encode(self.username + ':' + self.password)

_USERNAME = '_token'


class OAuth2(Basic):
  """Base class for turning OAuth2Credentials into suitable GCR credentials."""

  def __init__(
      self,
      creds,
      transport):
    """Constructor.

    Args:
      creds: the credentials from which to retrieve access tokens.
      transport: the http transport to use for token exchanges.
    """
    super(OAuth2, self).__init__(_USERNAME, 'does not matter')
    self._creds = creds
    self._transport = transport

  @property
  def password(self):
    # WORKAROUND...
    # The python oauth2client library only loads the credential from an
    # on-disk cache the first time 'refresh()' is called, and doesn't
    # actually 'Force a refresh of access_token' as advertised.
    # This call will load the credential, and the call below will refresh
    # it as needed.  If the credential is unexpired, the call below will
    # simply return a cache of this refresh.
    unused_at = self._creds.get_access_token(http=self._transport)

    # Most useful API ever:
    # https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={at}
    return self._creds.get_access_token(http=self._transport).access_token


class Helper(Basic):
  """This provider wraps a particularly named credential helper."""

  def __init__(
      self,
      name,
      registry):
    """Constructor.

    Args:
      name: the name of the helper, as it appears in the Docker config.
      registry: the registry for which we're invoking the helper.
    """
    super(Helper, self).__init__('does not matter', 'does not matter')
    self._name = name
    self._registry = registry.registry

  @property
  def suffix(self):
    # Invokes:
    #   echo -n {self._registry} | docker-credential-{self._name} get
    # The resulting JSON blob will have 'Username' and 'Secret' fields.

    p = subprocess.Popen(['docker-credential-{name}'.format(name=self._name),
                          'get'],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout = p.communicate(input=self._registry)[0]
    if p.returncode != 0:
      raise Exception('Error fetching credential for %s, exit status: %d\n%s'
                      % (self._name, p.returncode, stdout))

    blob = json.loads(stdout.decode())
    return base64.b64encode(blob['Username'] + ':' + blob['Secret'])


class Keychain(object):
  """Interface for resolving an image reference to a credential."""

  __metaclass__ = abc.ABCMeta  # For enforcing that methods are overriden.

  @abc.abstractmethod
  def Resolve(self, name):
    """Resolves the appropriate credential for the given registry.

    Args:
      name: the registry for which we need a credential.

    Returns:
      a Provider suitable for use with registry operations.
    """

_SCHEMES = ['', 'https://', 'http://']


def _GetUserHomeDir():
  if os.name == 'nt':
    # %HOME% has precedence over %USERPROFILE% for os.path.expanduser('~')
    # The Docker config resides under %USERPROFILE% on Windows
    return os.path.expandvars('%USERPROFILE%')
  else:
    return os.path.expanduser('~')


def _GetConfigDirectory():
  # Return the value of $DOCKER_CONFIG, if it exists, otherwise ~/.docker
  # see https://github.com/docker/docker/blob/master/cliconfig/config.go
  if os.environ.get('DOCKER_CONFIG') is not None:
    return os.environ.get('DOCKER_CONFIG')
  else:
    return os.path.join(_GetUserHomeDir(), '.docker')


class _DefaultKeychain(Keychain):
  """This implements the default docker credential resolution."""

  def Resolve(self, name):
    # TODO(user): Consider supporting .dockercfg, which was used prior
    # to Docker 1.7 and consisted of just the contents of 'auths' below.
    config_file = os.path.join(_GetConfigDirectory(), 'config.json')
    try:
      with open(config_file, 'r') as reader:
        cfg = json.loads(reader.read())
    except IOError:
      # If the file doesn't exist, fallback on anonymous auth.
      return Anonymous()

    # Per-registry credential helpers take precedence.
    cred_store = cfg.get('credHelpers', {})
    for prefix in _SCHEMES:
      if prefix + name.registry in cred_store:
        return Helper(cred_store[prefix + name.registry], name)

    # A global credential helper is next in precedence.
    if 'credsStore' in cfg:
      return Helper(cfg['credsStore'], name)

    # Lastly, the 'auths' section directly contains basic auth entries.
    auths = cfg.get('auths', {})
    for prefix in _SCHEMES:
      if prefix + name.registry in auths:
        entry = auths[prefix + name.registry]
        if 'auth' in entry:
          username, password = base64.b64decode(entry['auth']).split(':', 1)
          return Basic(username, password)
        elif 'username' in entry and 'password' in entry:
          return Basic(entry['username'], entry['password'])
        else:
          # TODO(user): Support identitytoken
          # TODO(user): Support registrytoken
          raise Exception(
              'Unsupported entry in "auth" section of Docker config: %s'
              % json.dumps(entry))

    return Anonymous()


# pylint: disable=invalid-name
DefaultKeychain = _DefaultKeychain()
