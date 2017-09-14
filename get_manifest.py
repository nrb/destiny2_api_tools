import os
import pprint
import requests
import zipfile

headers = {'X-API-Key': os.getenv('BUNGIE_API_KEY')}

MANIFEST_URL = 'https://bungie.net/Platform/Destiny2/Manifest/'

response = requests.get(MANIFEST_URL, headers=headers)
manifest = response.json()
pprint.pprint(manifest)
manifest_file_url = 'http://www.bungie.net' + manifest['Response']['mobileWorldContentPaths']['en']


r = requests.get(manifest_file_url)
with open('MANZIP', 'wb') as zip:
    zip.write(r.content)
print("Download complete")


# Extract the file contents, and rename the extracted file
# to 'Manifest.content'
with zipfile.ZipFile('MANZIP') as zip:
    name = zip.namelist()
    zip.extractall()
os.rename(name[0], 'Manifest.db')
print('Unzipped!')
