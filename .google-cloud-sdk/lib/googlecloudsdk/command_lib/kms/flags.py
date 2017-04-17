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
"""Helpers for parsing flags and arguments."""

from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.core import resources
from googlecloudsdk.core.util import times


# Collection names.
LOCATION_COLLECTION = 'cloudkms.projects.locations'
KEY_RING_COLLECTION = 'cloudkms.projects.locations.keyRings'
CRYPTO_KEY_COLLECTION = 'cloudkms.projects.locations.keyRings.cryptoKeys'
CRYPTO_KEY_VERSION_COLLECTION = (
    'cloudkms.projects.locations.keyRings.cryptoKeys.cryptoKeyVersions')


# Flags.
def AddLocationFlag(parser):
  def _CompletionCallback(parser):
    del parser  # Unused by Callback.
    return ['kms', 'locations', 'list', '--format=value(locationId)']
  parser.add_argument(
      '--location',
      completion_resource=LOCATION_COLLECTION,
      list_command_callback_fn=_CompletionCallback,
      help='The location of the requested resource.')


def AddKeyRingFlag(parser):
  parser.add_argument(
      '--keyring',
      completion_resource=KEY_RING_COLLECTION,
      help='The containing keyring.')


def AddCryptoKeyFlag(parser):
  parser.add_argument(
      '--key',
      completion_resource=CRYPTO_KEY_COLLECTION,
      help='The containing key.')


# Arguments
def AddKeyRingArgument(parser, help_action):
  parser.add_argument(
      'keyring',
      completion_resource=KEY_RING_COLLECTION,
      help='Name of the keyring %s.' % help_action)


def AddCryptoKeyArgument(parser, help_action):
  parser.add_argument(
      'key',
      completion_resource=CRYPTO_KEY_COLLECTION,
      help='Name of the key %s.' % help_action)


def AddCryptoKeyVersionArgument(parser, help_action):
  parser.add_argument(
      'version',
      completion_resource=CRYPTO_KEY_VERSION_COLLECTION,
      help='Name of the version %s.' % help_action)


def AddRotationPeriodFlag(parser):
  parser.add_argument(
      '--rotation-period',
      type=arg_parsers.Duration(lower_bound='1d'),
      help='Automatic rotation period of the key.')


def AddNextRotationTimeFlag(parser):
  parser.add_argument(
      '--next-rotation-time',
      type=arg_parsers.Datetime.Parse,
      help='Next automatic rotation time of the key.')


# Parsing.
def ParseLocationName(args):
  return resources.REGISTRY.Parse(args.location,
                                  collection=LOCATION_COLLECTION)


def ParseKeyRingName(args):
  return resources.REGISTRY.Parse(args.keyring, collection=KEY_RING_COLLECTION)


def ParseCryptoKeyName(args):
  return resources.REGISTRY.Parse(
      args.key, collection=CRYPTO_KEY_COLLECTION)


def ParseCryptoKeyVersionName(args):
  return resources.REGISTRY.Parse(
      args.version, collection=CRYPTO_KEY_VERSION_COLLECTION)


# Set proto fields from flags.
def SetRotationPeriod(args, crypto_key):
  if args.rotation_period is not None:
    crypto_key.rotationPeriod = '%ds' % args.rotation_period


def SetNextRotationTime(args, crypto_key):
  if args.next_rotation_time is not None:
    crypto_key.nextRotationTime = times.FormatDateTime(args.next_rotation_time)
