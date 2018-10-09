# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# this file creates a new csv export for a given kobo asset and gets a list of all previous exports

# import requests module
import requests
import sys
import os

# These variables can be overwritten with environment variables
# e.g.
# ```
# $>export KOBO_USER=newuser
# $>export KOBO_PASSW=newpassword
# $>export KOBO_ASSET=newasset
# $>export KOBO_URL=newurl
# ```
user = "username"
passw = "password"
asset = "koboassetid"
url = "https://kobo.humanitarianresponse.info/"
default_type = "csv"


def parse_env_variables():
    return os.getenv("KOBO_USER", user), \
           os.getenv("KOBO_PASSW", passw), \
           os.getenv("KOBO_ASSET", asset), \
           os.getenv("KOBO_URL", url), \

def create_export(type_="csv"):
    """
    Creates a new export.
    Prints the response of API if it's successful.
    :param type_: str.
    """

    if type_ not in ["csv", "json"]:
        print("Unsupported format")
        sys.exit()

    data = {
        "source": "{}assets/{}/".format(url, asset),
        "type": type_
    }
    response = requests.post(
        "{}exports/".format(url),
        data=data,
        auth=(user, passw))
    response.raise_for_status()

    print(response.status_code)
    print(response.text)

# see previous exports created
def list_exports():
    """
    Prints response of API for all exports
    :param type_: str.
    """
    response = _get_exports()
    print(response.json())

def latest_url():
    """
    Prints url of the latest created export.
    """
    response = _get_exports()
    json_ = response.json()
    result = json_.get("results")[-1]
    print(result.get("result"))

def _get_exports():
    payload = {"q": "source:{}".format(asset)}
    response = requests.get(
        "{}exports/".format(url),
        params=payload,
        auth=(user, passw))
    response.raise_for_status()

    return response

if __name__ == "__main__":

    # Overwrite local credentials with
    # environment variables if any
    user, passw, asset, url  = parse_env_variables()

    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            type_ = default_type
            if len(sys.argv) > 2:
                type_ = sys.argv[2]
            create_export(type_)
        elif sys.argv[1] == "list":
            list_exports()
        elif sys.argv[1] == "latest":
            latest_url()
        else:
            print("Invalid choice")
    else:
        create_export(default_type)