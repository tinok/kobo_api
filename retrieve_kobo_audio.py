#!/usr/bin/python

import json
import requests
import os
import sys
import urllib.request
from urllib.error import HTTPError

headers = { 'Authorization': 'Token [your token]' }

# read json list from here
assetlist = '{"[kpi asset id]": "[project title]"}'

# read json list from file, in case of many projects. Comment previous line out.
# with open('assets.json', 'r') as f:
#    assetlist=f.read()

# parse asset filecd 
assets = json.loads(assetlist)

# downloads audio file into a directory
def download_file(url, req_header):
    filename = url.split('/')[-1]
    file_path = os.path.join(dirname, filename)

    # checks and creates the directory if not exists 
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    # checkes if the file has already been downloaded
    # if found skips downloading
    if os.path.isfile(file_path):
        print('Skipping... File already exists.')
        return 'found' 

    try:
        response = requests.get(url, stream = True, headers=req_header)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size = 1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()

    return file_path

files_downloaded = 0
files_skipped = 0

for assetid in assets:
	kpiAssetID = assetid
	kpiTitle = assets[assetid]


	# directory name where the audio files be downloaded, using the kpiAssetID as a parent directory
	dirname = os.path.join('.', kpiTitle+'_'+kpiAssetID, 'audio_files')
	url = 'https://kf.kobotoolbox.org/api/v2/assets/' + kpiAssetID + '/data.json'

	try:
	    response = requests.get(url, headers=headers)
	    # If the response was successful, no Exception will be raised
	    response.raise_for_status()
	except HTTPError as http_err:
	    print(f'HTTP error occurred: {http_err}')
	except Exception as err:
	    print(f'Other error occurred: {err}')
	else:
	    # converts response as JSON object
	    response = response.json()
	    # iterates the response body to retrieve all the download urls and
	    # downloads the audio files.
	    for (key, value) in response.items():
	        if key == 'results':
	            for item in value:
	                for (key, value) in item.items():
	                    if key == '_attachments':
	                        for item in value:
	                            for (key, value) in item.items():
	                                if key == 'download_url' and (value.endswith('.mp3') or value.endswith('.wav') or value.endswith('.m4a') or value.endswith('.ogg') or value.endswith('.flac')):                                
	                                    audio_url = value
	                                    # temporary fix until URLs are fixed in kobocat
	                                    # file = download_file(audio_url, headers)
	                                    file = download_file(audio_url.replace('media_file=media_file=', 'media_file='), headers)
	                                    if file == 'found':
	                                        files_skipped += 1
	                                        pass
	                                    elif file is not None:
	                                        filename = file.split('/')[-1]
	                                        print(filename + " ===> Status: Download completed.")
	                                        files_downloaded += 1
	                                    else:
	                                        print("Status: Failed to download, try again.")
	                                        
print("Files downloaded:", files_downloaded)
print("Files skipped: ", files_skipped)
