# Python 3 only ^_^

import sys
import getpass
import requests

URL = 'http://kf.kobotoolbox.org/api/v2/assets/?format=json'

username = input(f'Username for "{URL}": ')
password = getpass.getpass()
auth = requests.auth.HTTPBasicAuth(username, password)

response = requests.get(URL, auth=auth)
for asset in response.json()['results']:
    # limit to surveys owned by the current user
    if asset['asset_type'] == 'survey' and asset['owner__username'] == username:
        yn = input(f'Remove "{asset["name"]}" ({asset["deployment__submission_count"]} submissions)? (y/n) ')
        if yn == 'y':
            del_resp = requests.delete(asset['url'], auth=auth)
            print(f'\t{del_resp.status_code}')