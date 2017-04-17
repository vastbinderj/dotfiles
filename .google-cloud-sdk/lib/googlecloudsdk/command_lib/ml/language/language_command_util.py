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
"""Flags for gcloud ml language commands."""

from googlecloudsdk.api_lib.ml.language import util


def RunLanguageCommand(feature, content_file=None, content=None,
                       language=None, content_type=None,
                       encoding_type=None):
  """Runs a gcloud ml language command.

  Args:
    feature: str, the name of the feature to request (e.g. 'extractEntities')
    content_file: str, the file to be used to analyze text.
    content: str, the text to be analyzed.
    language: str, the language of the input text.
    content_type: str, the format of the input text - 'PLAIN_TEXT' or 'HTML'.
    encoding_type: str, the encoding type to be used for calculating word
        offsets - 'UTF8', 'UTF16', 'UTF32', 'NONE'.

  Raises:
    ContentFileError: if content file can't be found and is not a GCS URL.
    ContentError: if content is given but empty.
    googlecloudsdk.api_lib.util.exceptions.HttpException: if the API returns
        an error.

  Returns:
    messages.AnnotateTextResponse: the response from the API.
  """
  client = util.LanguageClient()
  source = util.GetContentSource(content, content_file)
  return client.Annotate(feature, content_source=source, language=language,
                         content_type=content_type, encoding_type=encoding_type)


SERVICE_ACCOUNT_HELP = (
    'This command requires a service account from a project that has enabled '
    'the Natural Language API. To learn about using service accounts with the '
    'Natural Language API, please go to '
    'https://cloud.google.com/natural-language/docs/getting-started. '
    'Step 2 under the "Make an entity analysis request" section will give '
    'directions for using service accounts in gcloud.')

LANGUAGE_HELP = (
    'Currently English, Spanish, and Japanese are supported.')
