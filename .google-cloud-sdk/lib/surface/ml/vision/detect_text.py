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
"""Command to analyze text."""

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ml.vision import flags
from googlecloudsdk.command_lib.ml.vision import vision_command_util


class DetectText(base.Command):
  """Detect and extract text within an image.

  Detect and extract text within an image.

  Google Cloud Vision uses OCR (Optical Character Recognition) to detect text
  within an image, with support for a broad array of languages and automatic
  label detection.

  {language_hints}

  {auth_hints}
  """

  detailed_help = {'language_hints': flags.LANGUAGE_HINTS,
                   'auth_hints': vision_command_util.VISION_AUTH_HELP}

  @staticmethod
  def Args(parser):
    flags.AddVisionFlags(parser, with_max_results=False)
    flags.LANGUAGE_HINTS_FLAG.AddToParser(parser)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Raises:
      ImagePathError: if given image path does not exist and does not seem to be
          a remote URI.
      AnnotateException: if the annotation response contains an error.

    Returns:
      The results of the Annotate request.
    """
    return vision_command_util.RunVisionCommand(
        'TEXT_DETECTION',
        args.image_path,
        language_hints=args.language_hints
    )

  def Format(self, args):
    return 'json'
