# Getting Started

First, you'll need to set the `BUNGIE_API_KEY` environment variable.  See https://www.bungie.net/en/Application to get started with one.

Next, use `pipenv install` to install the requirements (just Requests for now)

Run `pipenv run python get_manifest.py` to download and unpack the manifest database onto your machine.

Then, use `pipenv run python main.py` to look up current vendor progression data.


# Usage

`pipenv run python main.py {platform} {username}` for fetching an account's vendor progression data

The platform should be one of `xbox`, `psn`, or `blizzard`.
