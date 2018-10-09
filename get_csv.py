# this file creates a new csv export for a given kobo asset and gets a list of all previous exports
# TODO: only return url of most recent csv export 

# import requests module
import requests

user = "username"
passw = "password"
asset = "koboassetid"
url = "https://kobo.humanitarianresponse.info/"

# create new csv export
def create_export():
	create_export = requests.post(
			url+'exports/', 
			data={'source': url+'assets/'+asset+'/', 'type': 'csv'}, 
			auth=(user, passw))
	print(create_export.status_code)
	print(create_export.text)

# see previous exports created
def list_exports():
	payload = {'q': 'source:'+asset}
	list_exports = requests.get(
			url+'exports/', 
			params=payload, 
			auth=(user, passw))
	print(list_exports.json())
