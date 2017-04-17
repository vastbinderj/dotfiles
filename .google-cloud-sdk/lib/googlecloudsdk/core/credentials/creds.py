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

"""Utilities to manage credentials."""

import abc
import base64
import json
import os

import enum

from googlecloudsdk.core import config
from googlecloudsdk.core import exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.credentials import devshell as c_devshell
import oauth2client
from oauth2client import client
from oauth2client import service_account
from oauth2client.contrib import gce as oauth2client_gce
from oauth2client.contrib import multistore_file


class Error(exceptions.Error):
  """Exceptions for this module."""


class UnknownCredentialsType(Error):
  """An error for when we fail to determine the type of the credentials."""
  pass


class CredentialStore(object):
  """Abstract definition of credential store."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def GetAccounts(self):
    """Get all accounts that have credentials stored for the CloudSDK.

    Returns:
      {str}, Set of accounts.
    """
    return NotImplemented

  @abc.abstractmethod
  def Load(self, account_id):
    return NotImplemented

  @abc.abstractmethod
  def Store(self, account_id, credentials):
    return NotImplemented

  @abc.abstractmethod
  def Remove(self, account_id):
    return NotImplemented

_CREDENTIAL_TABLE_NAME = 'credentials'


class _SqlCursor(object):
  """Context manager to access sqlite store."""

  def __init__(self, store_file):
    self._store_file = store_file
    self._connection = None
    self._cursor = None

  def __enter__(self):
    # TODO(b/36879084): Do not import sqlite upfront since some python
    # setups might not have it.
    import sqlite3  # pylint: disable=g-import-not-at-top
    self._connection = sqlite3.connect(
        self._store_file,
        isolation_level=None,  # Use autocommit mode.
        check_same_thread=True  # Only creating thread may use the connection.
    )
    self._cursor = self._connection.cursor()
    return self

  def __exit__(self, exc_type, unused_value, unused_traceback):
    if not exc_type:
      # Don't try to commit if exception is in progress.
      self._connection.commit()
    self._connection.close()

  def Execute(self, *args):
    return self._cursor.execute(*args)


class SqliteCredentialStore(CredentialStore):
  """Sqllite backed credential store."""

  def __init__(self, store_file):
    self._cursor = _SqlCursor(store_file)
    self._Execute(
        'CREATE TABLE IF NOT EXISTS "{}" '
        '(account_id TEXT PRIMARY KEY, value BLOB)'
        .format(_CREDENTIAL_TABLE_NAME))

  def _Execute(self, *args):
    with self._cursor as cur:
      return cur.Execute(*args)

  def GetAccounts(self):
    with self._cursor as cur:
      return set(key[0] for key in cur.Execute(
          'SELECT account_id FROM "{}" ORDER BY rowid'
          .format(_CREDENTIAL_TABLE_NAME)))

  def Load(self, account_id):
    with self._cursor as cur:
      item = cur.Execute(
          'SELECT value FROM "{}" WHERE account_id = ?'
          .format(_CREDENTIAL_TABLE_NAME), (account_id,)).fetchone()
    if item is not None:
      return FromJson(item[0])
    return None

  def Store(self, account_id, credentials):
    value = ToJson(credentials)
    self._Execute(
        'REPLACE INTO "{}" (account_id, value) VALUES (?,?)'
        .format(_CREDENTIAL_TABLE_NAME), (account_id, value))

  def Remove(self, account_id):
    self._Execute(
        'DELETE FROM "{}" WHERE account_id = ?'
        .format(_CREDENTIAL_TABLE_NAME), (account_id,))


_ACCESS_TOKEN_TABLE = 'access_tokens'


class AccessTokenCache(object):
  """Sqlite implementation of for access token cache."""

  def __init__(self, store_file):
    self._cursor = _SqlCursor(store_file)
    self._Execute(
        'CREATE TABLE IF NOT EXISTS "{}" '
        '(account_id TEXT PRIMARY KEY, '
        'access_token TEXT, '
        'token_expiry TIMESTAMP)'.format(_ACCESS_TOKEN_TABLE))

  def _Execute(self, *args):
    with self._cursor as cur:
      cur.Execute(*args)

  def Load(self, account_id):
    with self._cursor as cur:
      return cur.Execute(
          'SELECT access_token, token_expiry FROM "{}" WHERE account_id = ?'
          .format(_ACCESS_TOKEN_TABLE), (account_id,)).fetchone()

  def Store(self, account_id, access_token, token_expiry):
    self._Execute(
        'REPLACE INTO "{}" '
        '(account_id, access_token, token_expiry) VALUES (?,?,?)'
        .format(_ACCESS_TOKEN_TABLE),
        (account_id, access_token, token_expiry))

  def Remove(self, account_id):
    self._Execute(
        'DELETE FROM "{}" WHERE account_id = ?'
        .format(_ACCESS_TOKEN_TABLE), (account_id,))


class AccessTokenStore(client.Storage):
  """Oauth2client adapted for access token cache.

  This class works with Oauth2client model where access token is part of
  credential serialization format and get captured as part of that.
  By extending client.Storage this class pretends to serialize credentials, but
  only serializes access token.
  """

  def __init__(self, access_token_cache, account_id, credentials):
    """Sets up token store for given acount.

    Args:
      access_token_cache: AccessTokenCache, cache for access tokens.
      account_id: str, account for which token is stored.
      credentials: oauth2client.client.OAuth2Credentials, they are auto-updated
        with cached access token.
    """
    super(AccessTokenStore, self).__init__(lock=None)
    self._access_token_cache = access_token_cache
    self._account_id = account_id
    self._credentials = credentials

  def locked_get(self):
    access_token, token_expiry = self._access_token_cache.Load(self._account_id)
    self._credentials.access_token = access_token
    self._credentials.token_expiry = token_expiry
    return self._credentials

  def locked_put(self, credentials):
    self._access_token_cache.Store(self._account_id,
                                   self._credentials.access_token,
                                   self._credentials.token_expiry)

  def locked_delete(self):
    self._access_token_cache.Remove(self._account_id)


class CredentialStoreWithCache(CredentialStore):
  """Implements CredentialStore interface with access token caching."""

  def __init__(self, credential_store, access_token_cache):
    self._credential_store = credential_store
    self._access_token_cache = access_token_cache

  def GetAccounts(self):
    return self._credential_store.GetAccounts()

  def Load(self, account_id):
    credentials = self._credential_store.Load(account_id)
    if credentials is None:
      return None
    store = AccessTokenStore(self._access_token_cache, account_id, credentials)
    credentials.set_store(store)
    return store.get()

  def Store(self, account_id, credentials):
    store = AccessTokenStore(self._access_token_cache, account_id, credentials)
    credentials.set_store(store)
    store.put(credentials)
    return self._credential_store.Store(account_id, credentials)

  def Remove(self, account_id):
    self._credential_store.Remove(account_id)
    self._access_token_cache.Remove(account_id)


def GetCredentialStore(store_file=None, access_token_file=None):
  """Constructs credential store.

  Args:
    store_file: str, optional path to use for storage. If not specified
      config.Paths().credentials_path will be used.

    access_token_file: str, optional path to use for access token storage. Note
      that some implementations use store_file to also store access_tokens, in
      which case this argument is ignored.

  Returns:
    CredentialStore object.
  """

  if properties.VALUES.auth.use_sqlite_store.GetBool():
    store_file = store_file or os.path.join(
        config.Paths().global_config_dir, 'credentials.db')
    credential_store = SqliteCredentialStore(store_file)
    access_token_store_file = access_token_file or os.path.join(
        config.Paths().global_config_dir, 'access_token.db')
    access_token_cache = AccessTokenCache(access_token_store_file)
    return CredentialStoreWithCache(credential_store, access_token_cache)

  store_file = store_file or config.Paths().credentials_path
  return Oauth2ClientCredentialStore(store_file)


class Oauth2ClientCredentialStore(CredentialStore):
  """Implementation of credential sotore over oauth2client.multistore_file."""

  def __init__(self, store_file):
    self._store_file = store_file

  def GetAccounts(self):
    """Overrides."""
    all_keys = multistore_file.get_all_credential_keys(
        filename=self._store_file)

    return {self._StorageKey2AccountId(key) for key in all_keys}

  def Load(self, account_id):
    credential_store = self._GetStorageByAccountId(account_id)
    return credential_store.get()

  def Store(self, account_id, credentials):
    credential_store = self._GetStorageByAccountId(account_id)
    credential_store.put(credentials)
    credentials.set_store(credential_store)

  def Remove(self, account_id):
    credential_store = self._GetStorageByAccountId(account_id)
    credential_store.delete()

  def _GetStorageByAccountId(self, account_id):
    storage_key = self._AcctountId2StorageKey(account_id)
    return multistore_file.get_credential_storage_custom_key(
        filename=self._store_file, key_dict=storage_key)

  def _AcctountId2StorageKey(self, account_id):
    """Converts account id into storage key."""
    all_storage_keys = multistore_file.get_all_credential_keys(
        filename=self._store_file)
    matching_keys = [k for k in all_storage_keys if k['account'] == account_id]
    if not matching_keys:
      return {'type': 'google-cloud-sdk', 'account': account_id}

    # We do not expect any other type keys in the credential store. Just in case
    # somehow they occur:
    #  1. prefer key with no type
    #  2. use google-cloud-sdk type
    #  3. use any other
    # Also log all cases where type was present but was not google-cloud-sdk.
    right_key = matching_keys[0]
    for key in matching_keys:
      if 'type' in key:
        if key['type'] == 'google-cloud-sdk' and 'type' in right_key:
          right_key = key
        else:
          log.file_only_logger.warn(
              'Credential store has unknown type [{0}] key for account [{1}]'
              .format(key['type'], key['account']))
      else:
        right_key = key
    if 'type' in right_key:
      right_key['type'] = 'google-cloud-sdk'
    return right_key

  def _StorageKey2AccountId(self, storage_key):
    return storage_key['account']


class CredentialType(enum.Enum):
  """Enum of credential types managed by gcloud."""

  UNKNOWN = (0, 'unknown', False)
  USER_ACCOUNT = (1, client.AUTHORIZED_USER, True)
  SERVICE_ACCOUNT = (2, client.SERVICE_ACCOUNT, True)
  P12_SERVICE_ACCOUNT = (3, 'service_account_p12', True)
  DEVSHELL = (4, 'devshell', False)
  GCE = (5, 'gce', False)

  def __init__(self, type_id, key, is_serializable):
    self.type_id = type_id
    self.key = key
    self.is_serializable = is_serializable

  @staticmethod
  def FromTypeKey(key):
    for cred_type in CredentialType:
      if cred_type.key == key:
        return cred_type
    return CredentialType.UNKNOWN

  @staticmethod
  def FromCredentials(creds):
    if isinstance(creds, c_devshell.DevshellCredentials):
      return CredentialType.DEVSHELL
    if isinstance(creds, oauth2client_gce.AppAssertionCredentials):
      return CredentialType.GCE
    if isinstance(creds, service_account.ServiceAccountCredentials):
      if getattr(creds, '_private_key_pkcs12', None) is not None:
        return CredentialType.P12_SERVICE_ACCOUNT
      return CredentialType.SERVICE_ACCOUNT
    if getattr(creds, 'refresh_token', None) is not None:
      return CredentialType.USER_ACCOUNT
    return CredentialType.UNKNOWN


def ToJson(credentials):
  """Given Oauth2client credentials return library independent json for it."""
  creds_type = CredentialType.FromCredentials(credentials)
  if creds_type == CredentialType.USER_ACCOUNT:
    creds_dict = {
        'type': creds_type.key,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'refresh_token': credentials.refresh_token
    }
  elif creds_type == CredentialType.SERVICE_ACCOUNT:
    creds_dict = credentials.serialization_data
  elif creds_type == CredentialType.P12_SERVICE_ACCOUNT:
    # pylint: disable=protected-access
    creds_dict = {
        'client_email': credentials._service_account_email,
        'type': creds_type.key,
        'private_key': base64.b64encode(credentials._private_key_pkcs12),
        'password': credentials._private_key_password
    }
  else:
    raise UnknownCredentialsType(creds_type)
  return json.dumps(creds_dict, sort_keys=True,
                    indent=2, separators=(',', ': '))


def FromJson(json_value):
  """Returns Oauth2client credentials from library independend json format."""
  json_key = json.loads(json_value)
  cred_type = CredentialType.FromTypeKey(json_key['type'])
  if cred_type == CredentialType.SERVICE_ACCOUNT:
    cred = service_account.ServiceAccountCredentials.from_json_keyfile_dict(
        json_key, scopes=config.CLOUDSDK_SCOPES)
    cred.user_agent = cred._user_agent = config.CLOUDSDK_USER_AGENT
  elif cred_type == CredentialType.USER_ACCOUNT:
    cred = client.GoogleCredentials(
        access_token=None,
        client_id=json_key['client_id'],
        client_secret=json_key['client_secret'],
        refresh_token=json_key['refresh_token'],
        token_expiry=None,
        token_uri=oauth2client.GOOGLE_TOKEN_URI,
        user_agent=config.CLOUDSDK_USER_AGENT)
  elif cred_type == CredentialType.P12_SERVICE_ACCOUNT:
    # pylint: disable=protected-access
    cred = service_account.ServiceAccountCredentials._from_p12_keyfile_contents(
        service_account_email=json_key['client_email'],
        private_key_pkcs12=base64.b64decode(json_key['private_key']),
        private_key_password=json_key['password'],
        scopes=config.CLOUDSDK_SCOPES)
    cred.user_agent = cred._user_agent = config.CLOUDSDK_USER_AGENT
  else:
    raise UnknownCredentialsType(json_key['type'])
  return cred
