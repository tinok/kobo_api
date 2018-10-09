# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# this file creates a new csv export for a given kobo asset and gets a list of all previous exports
# TODO: only return url of most recent csv export 

# import requests module
import requests
import sys

user = "username"
passw = "password"
asset = "koboassetid"
url = "https://kobo.humanitarianresponse.info/"
default_type = "csv"

# create new csv export
def create_export(type_="csv"):

    if type_ not in ["csv", "json"]:
        print("Unsupported format")
        sys.exit()

    data = {
        "source": "{}assets/{}/".format(url, asset),
        "type": type_
    }
    create_export = requests.post(
            "{}exports/".format(url),
            data=data,
            auth=(user, passw))
    print(create_export.status_code)
    print(create_export.text)

# see previous exports created
def list_exports():
    payload = {"q": "source: {}".format(asset)}
    list_exports = requests.get(
            url+'exports/',
            params=payload,
            auth=(user, passw))
    print(list_exports.json())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            type_ = default_type
            if len(sys.argv) > 2:
                type_ = sys.argv[2]

            create_export(type_)

        elif sys.argv[1] == "export":
            list_exports()
        else:
            print("Invalid choice")
    else:
        create_export(default_type)