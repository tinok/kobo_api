# Python 3 only ^_^

import sys
import getpass
import requests

URL = 'http://kf.kobotoolbox.org/api/v2/assets/?format=json'

username = input('Username for "{}": '.format(URL))
password = getpass.getpass()
auth = requests.auth.HTTPBasicAuth(username, password)

response = requests.get(URL, auth=auth)
for asset in response.json()['results']:
    yn = input(f'Remove "{asset["name"]}" ({asset["uid"]})? (y/n) ')
    if yn == 'y':
        del_resp = requests.delete(asset['url'], auth=auth)
        print(f'\t{del_resp.status_code}')
