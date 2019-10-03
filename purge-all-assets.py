import sys
import getpass
import requests

URL = 'http://kf.kobotoolbox.org/assets/?format=json'

username = raw_input('Username for "{}": '.format(URL))
password = getpass.getpass()
auth = requests.auth.HTTPBasicAuth(username, password)

response = requests.get(URL, auth=auth)
for asset in response.json()['results']:
    # raw_input() can't write unicode. Can you believe it?
    # https://bugs.python.org/issue7768
    sys.stdout.write(
        u'Remove "{}" ({})? (y/n) '.format(asset['name'], asset['uid'])
    )
    yn = raw_input()
    if yn == 'y':
        del_resp = requests.delete(asset['url'], auth=auth)
        print '\t', del_resp.status_code
