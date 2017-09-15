# Getting Started

First, you'll need to set the `BUNGIE_API_KEY` environment variable.  See https://www.bungie.net/en/Application to get started with one.

Next, use `pipenv install` to install the requirements (just Requests for now)

Run `pipenv run python get_manifest.py` to download and unpack the manifest database onto your machine. If you've already got a manifest file, it won't redownload, but you can run `pipenv run python get_manifest.py update` to manually update.

Then, use `pipenv run python main.py` to look up current vendor progression data.


# Usage

`pipenv run python main.py {platform} {username}` for fetching an account's vendor progression data

The platform should be one of `xbox`, `psn`, or `blizzard`.

# Getting an interactive shell

The `-s` or `--shell` option to `main.py` will get you an interactive shell. This is a Python REPL with some Destiny inforation pre-loaded into the context. Use `h()` to list the available variables.
