import argparse
import code
import os
import json
import requests
import sqlite3
import sys

BASE_URL = 'https://bungie.net/Platform/Destiny2/'


def dump(thing):
    """Convenience function for printing stuff"""
    import pprint
    pprint.pprint(thing)


def get_table_data(conn, data_type):
    cur = conn.cursor()
    query_tmpl = 'SELECT json from Destiny{data_type}Definition'

    def clean(table_name):
        cleaned = ''.join(chr for chr in table_name if chr.isalnum())
        return cleaned.capitalize()
    table_name = clean(data_type)

    query = query_tmpl.format(data_type=table_name)
    cur.execute(query)

    rows = cur.fetchall()

    all_data = {}
    for row in rows:
        data = json.loads(row[0])
        all_data[data['hash']] = data
    return all_data


def get_vendor_data(conn):
    vendors = get_table_data(conn, 'vendor')

    return vendors


def get_faction_data(conn):
    factions = get_table_data(conn, 'faction')

    return factions


def get_milestone_data(conn):
    milestones = get_table_data(conn, 'milestone')

    return milestones


def get_inventoryitem_data(conn):
    items = get_table_data(conn, 'inventoryItem')

    return items


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

        remaining = int(next_level) - int(current)
        tokens_needed = int(remaining // token_value)

        green_mats_needed = int(remaining // 35)

        display = '{name}: {current} / {next_level} ({tokens_needed} tokens/blue mats or {greens} planet mats)'
        if f_name == 'Gunsmith':
            green_mats_needed = int(remaining // 25)
            display = '{name}: {current} / {next_level} ({tokens_needed} Gunsmith Materials, or {greens} Telemetries)'
        if f_name == 'Vanguard Research':
            display = '{name}: {current} / {next_level} ({tokens_needed} tokens)'
        print(display.format(name=f_name, current=current,
                             next_level=next_level,
                             tokens_needed=tokens_needed,
                             greens=green_mats_needed))


def lookup_token_values(faction_name):
    exceptions = {
        'Gunsmith': 2000 / 30,
        'Vanguard Research': 7000 / 7
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
    available_vars = '\n  '.join(context.keys())

    banner = ("Type 'h()' for help on destiny variables.\n"
              "Use 'clear()' to clear the screen")

    def h():
        print("Available variables:\n  " + available_vars)

    context['h'] = h
    context['clear'] = _clear

    code.interact(banner=banner, local=context)


def _clear():
    print("\x1b[2J\x1b[H")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('platform',
                        choices=['xbox', 'psn', 'blizzard'],
                        help='The platform the user plays on')
    parser.add_argument('user',
                        help='Username associated with the Destiny 2 account')
    parser.add_argument('-s', '--shell',
                        action='store_true',
                        help="Launch a shell with the given account's data loaded")
    return parser.parse_args(args)


def parse_platform(platform_id):
    platforms = {
        'none': 0,
        'xbox': 1,
        'psn': 2,
        'blzzard': 4,
        'battlenet': 4,
        'tigerdemon': 10,
        'bungienext': 254,
        'all': -1,
    }

    return platforms[platform_id.lower()]


def main():
    args = parse_args(sys.argv[1:])

    platform = parse_platform(args.platform)

    profile = get_profile(platform, args.user)
    progs = profile['characterProgressions']['data']
    characters = profile['characters']['data']

    conn = sqlite3.connect('Manifest.db')
    vendors = get_vendor_data(conn)
    factions = get_faction_data(conn)
    milestones = get_milestone_data(conn)
    items = get_inventoryitem_data(conn)
    conn.close()

    if args.shell:
        ctx = {'profile': profile, 'progs': progs, 'chars': characters,
               'factions': factions, 'vendors': vendors,
               'milestones': milestones, 'items': items}
        launch_shell(ctx)
        return

    for _, char in characters.items():
        char_class = get_characters_class(int(char['classType']))
        print(char_class)
        print('-----')
        chars_progs = progs[char['characterId']]
        show_faction_progress(chars_progs, factions)
        print('\n')


if __name__ == '__main__':
    main()
