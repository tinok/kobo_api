# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# This file creates a new csv export for a given kobo asset and gets a list of all previous exports
# For help run `python get_csv.py -h'

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
USERNAME = "username"
PASSWD = "password"
ASSET = "koboassetid"
DOMAIN = "https://kobo.humanitarianresponse.info/"

# These variables define the default export. Each value can be overwritten when running the `create' command
# e.g. `create -t csv -l 'English (en_US)' -f true'. 
DEFAULT_TYPE = "csv"
DEFAULT_LANG = "xml"
DEFAULT_FIELDS_FROM_ALL_VERSIONS = "true"
DEFAULT_HIERARCHY_IN_LABELS = "false"
DEFAULT_GROUP_SEP = "/"

VALID_ARGUMENTS = {
    "create": {
        "asset": ["-a", "--asset"],
        "domain": ["-d", "--domain"],
        "all_fields": ["-f", "--fields"],
        "group_sep": ["-g", "--group-sep"],
        "hierarchy": ["-H", "--hierarchy"],
        "lang": ["-l", "--lang"],
        "passwd": ["-p", "--passwd"],
        "type_": ["-t", "--type"],
        "username": ["-u", "--username"]
    },
    "list": {
        "asset": ["-a", "--asset"],
        "domain": ["-d", "--domain"],
        "passwd": ["-p", "--passwd"],
        "username": ["-u", "--username"]
    },
    "latest": {
        "asset": ["-a", "--asset"],
        "domain": ["-d", "--domain"],
        "passwd": ["-p", "--passwd"],
        "username": ["-u", "--username"]
    }
}


def create_export(asset, username, passwd, domain, type_=DEFAULT_TYPE, lang=DEFAULT_LANG,
                  all_fields=DEFAULT_FIELDS_FROM_ALL_VERSIONS,
                  hierarchy=DEFAULT_HIERARCHY_IN_LABELS, group_sep=DEFAULT_GROUP_SEP):
    """
    Creates a new export.
    Prints the response of API if it's successful.

    :param asset: str.
    :param username: str.
    :param passwd: str.
    :param domain: str.
    :param type_: str.
    :param lang: str.
    :param all_fields: str. true|false
    :param hierarchy: str. true|false
    :param group_sep: str. "/"
    """

    if type_ not in ["csv", "xls", "spss_labels"]:
        print("Only csv, xls, and spss_labels are supported with this method")
        sys.exit()

    data = {
        "source": "{}assets/{}/".format(domain, asset),
        "type": type_,
        "lang": lang,
        "fields_from_all_versions": _str_bool(all_fields),
        "hierarchy_in_labels": _str_bool(hierarchy),
        "group_sep": group_sep
    }

    response = requests.post(
        "{}exports/".format(domain),
        data=data,
        auth=(username, passwd))
    response.raise_for_status()

    print(response.status_code)
    print(response.text)


def list_exports(asset, username, passwd, domain):
    """
    Prints response of API for all exports
    """
    response = _get_exports(asset, username, passwd, domain)
    print(response.json())


def latest_url(asset, username, passwd, domain):
    """
    Prints url of the latest created export.
    """
    response = _get_exports(asset, username, passwd, domain)
    json_ = response.json()
    result = json_.get("results")[-1]
    print(result.get("result"))


def _bad_syntax():
    print("Bad syntax. Please `python get_csv.py -h` for help")
    sys.exit()


def _help():
    print(("Usage: python get_csv.py [command] [options]\n"
           "\n"
           "    Command 'create'\n"
           "        Create a new export\n"
           "\n"
           "        Options:\n"
           "          -a, --asset\n"
           "                UID of the asset\n"
           "          -d, --domain\n"
           "                Domain name\n"
           "          -f, --fields\n"
           "                Include fields from all versions. Default: `true`\n"
           "          -g, --group-sep\n"
           "                Groups separator. Default: `/`\n"
           "          -H, --hierarchy\n"
           "                Hierarchy in labels. Default: `false`\n"
           "          -l, --lang\n"
           "                Language. Default: `xml`\n"
           "          -p, --passwd\n"
           "                User's password\n"    
           "          -t, --type\n"
           "                Type of the export. `xls` or `csv` or `spss_labels`. Default: `csv`\n"
           "          -u, --username\n"
           "                User's username\n"
           "\n"
           "    Command 'list'\n"
           "        Print response of API for all exports\n"
           "\n"
           "        Options:\n"
           "          -a, --asset\n"
           "                UID of the asset\n"
           "          -d, --domain\n"
           "                Domain name\n"
           "          -p, --passwd\n"
           "                User's password\n"
           "          -u, --username\n"
           "                User's username\n"
           "\n"
           "    Command 'latest'\n"
           "        Print url of latest export\n"
           "\n"
           "        Options:\n"
           "          -a, --asset\n"
           "                UID of the asset\n"
           "          -d, --domain\n"
           "                Domain name\n"
           "          -p, --passwd\n"
           "                User's password\n"
           "          -u, --username\n"
           "                User's username"))

    sys.exit()


def _get_exports(asset, username, passwd, domain):
    payload = {"q": "source:{}".format(asset)}
    response = requests.get(
        "{}exports/".format(domain),
        params=payload,
        auth=(username, passwd))
    response.raise_for_status()

    return response


def _parse_arguments():
    """
    Parses command line arguments to detect which method to call and which parameters to pass to this method
    :return: tuple. (method, kwargs)
    """

    # Overwrite local credentials with
    # environment variables if any
    username, passwd, asset, domain  = _parse_env_variables()
    kwargs = {
        "username": username,
        "passwd": passwd,
        "asset": asset,
        "domain": domain
    }
    method_ = "create"

    def _find_key(method_, needle):
        for key, options in VALID_ARGUMENTS.get(method_).items():
            if needle in options:
                return key
        return None

    if len(sys.argv) > 1:
        method_ = sys.argv[1]
        if method_ in ["-h", "--help"]:
            _help()
        elif method_ not in VALID_ARGUMENTS.keys():
            _bad_syntax()

        try:
            for index, arg in enumerate(sys.argv[2::2]):
                key = _find_key(method_, arg)
                if key:
                    kwargs[key] = sys.argv[index * 2 + 3]
                else:
                    _bad_syntax()
        except Exception as e:
            print(str(e))
            _bad_syntax()

    return method_, kwargs


def _parse_env_variables():
    return os.getenv("KOBO_USER", USERNAME), \
           os.getenv("KOBO_PASSW", PASSWD), \
           os.getenv("KOBO_ASSET", ASSET), \
           os.getenv("KOBO_DOMAIN", DOMAIN), \


def _str_bool(value):

    if isinstance(value, bool):
        return "true" if value else "false"
    else:
        return "true" if str(value).lower() == "true" else "false"

if __name__ == "__main__":

    method, kwargs = _parse_arguments()
    methods = {
        "create": create_export,
        "list": list_exports,
        "latest": latest_url
    }
    methods[method](**kwargs)