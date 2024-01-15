# source: https://github.com/unconst/ImageSubnet/blob/main/utils.py
# The MIT License (MIT)
# Copyright © 2023 Unconst

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import requests
import bittensor as bt
import sys

PATH_TO_REPO = "https://raw.githubusercontent.com/bittranslateio/bittranslate-test/main/VERSION"

def check_for_updates(no_restart):
    try:
        bt.logging.info("Checking for updates...")
        response = requests.get(
            PATH_TO_REPO
        )
        response.raise_for_status()
        try:
            # load version from VERSION file
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")) as f:
                __version__ = f.read().strip()
                # convert to list of ints
                __version__ = [int(v) for v in __version__.split(".")]
            latest_version = response.text.strip()
            latest_version = [int(v) for v in latest_version.split(".")]
            bt.logging.info(f"Current version: {__version__}")
            bt.logging.info(f"Latest version: {latest_version}")
            if latest_version > __version__:
                bt.logging.info("A newer version of BitTranslate is available. Downloading...")
                # download latest version with git pull
                os.system("git pull")
                # checking local VERSION
                with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")) as f:
                    new__version__ = f.read().strip()
                    # convert to list of ints
                    new__version__ = [int(v) for v in new__version__.split(".")]
                    if new__version__ == latest_version and new__version__ > __version__:
                        try:
                            os.system("pip install -e .")
                        except Exception as e:
                            bt.logging.error("Failed to run 'pip install -e . '".format(e))

                        if not no_restart:
                            bt.logging.info("BitTranslate updated successfully. Restarting...")
                            bt.logging.info(f"Running: {sys.executable} {sys.argv}")
                            try:
                                # add an argument to the end of the command to prevent infinite loop
                                os.execv(sys.executable, [sys.executable] + sys.argv + ["--no-restart"])
                            except Exception as e:
                                bt.logging.error("Error restarting process'".format(e))
                        else:
                            bt.logging.info("BitTranslate has been updated successfully. Restart to apply changes.")
                    else:
                        bt.logging.error("BitTranslate git pull failed you will need to manually update and restart for latest code.")
        except Exception as e:
            bt.logging.error("Failed to convert response to json: {}".format(e))
            bt.logging.info("Response: {}".format(response.text))
    except Exception as e:
        bt.logging.error("Failed to check for updates: {}".format(e))