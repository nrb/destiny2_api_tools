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

# Output

Output will look something like this:

```
Warlock
-----
The Crucible: 100 / 2000 (19 tokens/blue mats or 54 planet mats)
Fragmented Researcher: 375 / 2000 (16 tokens/blue mats or 46 planet mats)
Dead Zone Scout: 105 / 2000 (18 tokens/blue mats or 54 planet mats)
Field Commander: 345 / 2000 (16 tokens/blue mats or 47 planet mats)
Gunsmith: 325 / 2000 (25 Gunsmith Materials)
Vanguard Research: 2000 / 7000 (2 tokens)
Leviathan: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Exodus Black AI: 1240 / 2000 (7 tokens/blue mats or 21 planet mats)
Vanguard Tactical: 600 / 2000 (14 tokens/blue mats or 40 planet mats)


Hunter
-----
The Crucible: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Fragmented Researcher: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Dead Zone Scout: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Field Commander: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Gunsmith: 0 / 2000 (29 Gunsmith Materials)
Vanguard Research: 0 / 7000 (2 tokens)
Leviathan: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Exodus Black AI: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Vanguard Tactical: 0 / 2000 (20 tokens/blue mats or 57 planet mats)


Titan
-----
The Crucible: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Fragmented Researcher: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Dead Zone Scout: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Field Commander: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Gunsmith: 0 / 2000 (29 Gunsmith Materials)
Vanguard Research: 0 / 7000 (2 tokens)
Leviathan: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Exodus Black AI: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
Vanguard Tactical: 0 / 2000 (20 tokens/blue mats or 57 planet mats)
```
