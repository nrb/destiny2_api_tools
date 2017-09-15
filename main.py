import code
import os
import json
import requests
import sqlite3
import sys

BASE_URL = 'https://bungie.net/Platform/Destiny2/'


def get_vendor_data():
    con = sqlite3.connect('Manifest.db')

    cur = con.cursor()

    cur.execute('SELECT json from DestinyVendorDefinition')
    vendor_rows = cur.fetchall()

    vendors = {}
    for row in vendor_rows:
        data = json.loads(row[0])
        vendors[data['hash']] = data

    return vendors


def get_faction_data():
    con = sqlite3.connect('Manifest.db')
    cur = con.cursor()

    cur.execute('SELECT json from DestinyFactionDefinition')
    faction_rows = cur.fetchall()

    factions = {}

    for row in faction_rows:
        data = json.loads(row[0])
        factions[data['hash']] = data

    return factions


def get_milestone_data():
    con = sqlite3.connect('Manifest.db')
    cur = con.cursor()

    cur.execute('SELECT json from DestinyMilestoneDefinition')
    milestone_rows = cur.fetchall()

    milestones = {}
    for row in milestone_rows:
        data = json.loads(row[0])
        milestones[data['hash']] = data

    return milestones


def get_milestone_rewards(milestones):
    for _, data in milestones.items():
        pass


def get_characters_class(class_type):
    class_types = [
        'Titan',
        'Hunter',
        'Warlock',
        'Unknown',
    ]

    return class_types[class_type]


def show_faction_progress(character, factions):
    for _, data in character['factions'].items():
        # Interesting data keys:
        #   progressToNextLevel
        #   nextLevelAt
        #   currentProgress
        faction = factions[data['factionHash']]
        f_name = faction['displayProperties']['name']
        if f_name == 'Classified':
            continue
        next_level = data['nextLevelAt']
        current = data['progressToNextLevel']

        token_value = lookup_token_values(f_name)
        # print('{}: {}'.format(f_name, token_value))

        # blue mats = 100
        # green mats = 35

        remaining = int(next_level) - int(current)
        tokens_needed = remaining / token_value

        green_mats_needed = remaining / 35

        display = '{name}: {current} / {next_level} ({tokens_needed} tokens/blue mats or {greens} planet mats)'
        if f_name == 'Gunsmith':
            display = '{name}: {current} / {next_level} ({tokens_needed} Gunsmith Materials)'
        if f_name == 'Vanguard Research':
            display = '{name}: {current} / {next_level} ({tokens_needed} tokens)'
        print(display.format(name=f_name, current=current,
                             next_level=next_level,
                             tokens_needed=tokens_needed,
                             greens=green_mats_needed))


def lookup_token_values(faction_name):
    exceptions = {
        'Gunsmith': 2000 / 30,
        'Vanguard Research': 7000 / 3
    }
    if exceptions.get(faction_name, None):
        return exceptions[faction_name]
    return 2000 / 20


def get_membership_id(member_type, username):
    GET_ID_URL = (BASE_URL + 'SearchDestinyPlayer/' +
                  '{membershipType}/{displayName}/')
    get_id_url = GET_ID_URL.format(membershipType=member_type,
                                   displayName=username)
    headers = {'X-API-Key': os.getenv('BUNGIE_API_KEY')}
    response = requests.get(get_id_url, headers=headers)
    member_id = response.json()['Response'][0]['membershipId']
    return member_id


def get_profile(member_type, username):
    GET_PROFILE_URL = (BASE_URL +
                       '{membershipType}/Profile/{destinyMembershipId}/')

    headers = {'X-API-Key': os.getenv('BUNGIE_API_KEY')}
    member_id = get_membership_id(member_type, username)
    get_profile_url = GET_PROFILE_URL.format(membershipType=member_type,
                                             destinyMembershipId=member_id)
    response = requests.get(get_profile_url, headers=headers,
                            params={'components': '200,202'})
    r = response.json()
    profile = r['Response']
    return profile


def launch_shell(context):
    code.interact(local=context)


def _clear():
    print("\x1b[2J\x1b[H")


def main():
    member_type = '2'
    user = 'GUUBU'
    args = sys.argv[1:]
    if len(args) == 2:
        member_type = args[0]
        user = args[1]
    profile = get_profile(member_type, user)
    progs = profile['characterProgressions']['data']
    characters = profile['characters']['data']

    factions = get_faction_data()
    vendors = get_vendor_data()
    milestones = get_milestone_data()

    if len(args) == 1 and args[0] == 'shell':
        ctx = {'profile': profile, 'progs': progs, 'chars': characters,
               'factions': factions, 'vendors': vendors,
               'milestones': milestones, 'clear': _clear}
        launch_shell(ctx)
        return

    for _, char in characters.items():
        char_class = get_characters_class(int(char['classType']))
        print(char_class)
        print('-----')
        chars_progs = progs[char['characterId']]
        show_faction_progress(chars_progs, get_faction_data())
        print('\n')


if __name__ == '__main__':
    main()
