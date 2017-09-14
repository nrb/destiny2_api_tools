import json
import pprint
import sqlite3

con = sqlite3.connect('Manifest.db')

cur = con.cursor()

vendor_data = {}

cur.execute('SELECT json from DestinyVendorDefinition')
vendor_rows = cur.fetchall()

vendors = [json.loads(row[0]) for row in vendor_rows]

pprint.pprint(vendors[0].keys())

cur.execute('SELECT json from DestinyFactionDefinition')
faction_rows = cur.fetchall()

factions = {}

for row in faction_rows:
    data = json.loads(row[0])
    factions[data['hash']] = data

for vendor in vendors:
    if vendor['factionHash'] != 0:
        vendor_faction = factions[vendor['factionHash']]
        print(vendor_faction['displayProperties']['name'])
