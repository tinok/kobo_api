# this file creates a new csv export for a given kobo asset and gets a list of all previous exports
# TODO: only return url of most recent csv export 

# import requests module
import requests

user = "username"
passw = "password"
asset = "koboassetid"

# create new csv export
def create_csv():
	create_export = requests.post(
			'https://kobo.humanitarianresponse.info/exports/', 
			data={'source': 'https://kobo.humanitarianresponse.info/assets/'+asset+'/', 'type': 'csv'}, 
			auth=(user, passw))
	print(create_export.status_code)
	print(create_export.text)

# see previous exports created
def exports_list():
	payload = {'q': 'source:'+asset}
	get_exports = requests.get(
			'https://kobo.humanitarianresponse.info/exports/', 
			params=payload, 
			auth=(user, passw))
	print(get_exports.json())
