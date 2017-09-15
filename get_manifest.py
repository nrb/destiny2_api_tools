import os
import requests
import sys
import tempfile
import zipfile

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

headers = {'X-API-Key': os.getenv('BUNGIE_API_KEY')}

MANIFEST_URL = 'https://bungie.net/Platform/Destiny2/Manifest/'

response = requests.get(MANIFEST_URL, headers=headers)
manifest = response.json()
manifest_file_url = 'http://www.bungie.net' + manifest['Response']['mobileWorldContentPaths']['en']

target = pathlib.Path('./Manifest.db')

args = sys.argv[1:]

if target.exists() and 'update' not in args:
    print("Manifest.db already present, nothing to do!")
    sys.exit(0)

temp_zip = tempfile.NamedTemporaryFile(mode='wb')

r = requests.get(manifest_file_url)
temp_zip.write(r.content)
print("Download complete")


# Extract the file contents, and rename the extracted file
# to 'Manifest.content'
with zipfile.ZipFile(temp_zip.name) as zip:
    name = zip.namelist()
    zip.extractall()
os.rename(name[0], 'Manifest.db')
print('Unzipped as Manifest.db')
