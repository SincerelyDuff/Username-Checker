<div align="center">

<img src="checker.png" alt="checker preview" width="700"/>

<br/>

# username-checker

**Multi-platform username checker — find available usernames fast**

[!\[Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)](https://python.org)
[!\[Version](https://img.shields.io/badge/Version-1.1-blue?style=flat-square)](#)
[!\[Platforms](https://img.shields.io/badge/Platforms-8-cyan?style=flat-square)](#platforms)
[!\[License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)
[!\[Discord](https://img.shields.io/badge/Discord-Join-7289da?style=flat-square&logo=discord)](https://discord.gg/c95uE5ejff)

<br/>

[**Download**](#installation) • [**Platforms**](#platforms) • [**Usage**](#usage) • [**Discord**](https://discord.gg/8EEAR8qtdx)

</div>

\---

## preview

<div align="center">
<img src="preview.png" alt="checker running" width="650"/>
</div>

\---



</div>

\---

## platforms

|Platform|Method|Min Length|Speed|
|-|-|-|-|
|Roblox|Official API|3 letters|Fast|
|Minecraft|Mojang API|3 letters|Fast|
|TikTok|Profile pages|4 letters|Medium|
|YouTube|Profile pages|4 letters|Medium|
|Twitch|Profile pages|4 letters|Fast|
|GitHub|Official API|3 letters|Slow (rate limited)|
|Twitter / X|Profile pages|4 letters|Slow (rate limited)|
|guns.lol|Profile pages|3 letters|Fast|

\---

## features

* 8 platforms supported in one tool
* 3, 4, 5 and 6 letter username checking
* letters only / letters + numbers / letters + underscore / all combined
* load your own custom `.txt` wordlist
* live estimated time remaining while checking
* run again option after finishing — no need to restart
* multithreaded — up to 50 threads
* auto saves results to a separate file per platform
* colored terminal UI
* works on Windows, Mac and Linux

\---

## installation

### Windows

**1. clone the repo**

```
git clone https://github.com/40oo/username-checker.git
cd username-checker
```

**2. install dependencies**

```
pip install requests colorama
```

**3. run**

```
python username\\\\\\\_checker.py
```

\---

### Linux

**1. clone the repo**

```
git clone https://github.com/40oo/username-checker.git
cd username-checker
```

**2. install dependencies**

```
pip3 install requests colorama --break-system-packages
```

**3. run**

```
python3 username\\\\\\\\\\\\\\\_checker.py
```

\---

### macOS

**1. clone the repo**

```
git clone https://github.com/40oo/username-checker.git
cd username-checker
```

**2. install dependencies**

```
pip3 install requests colorama
```

**3. run**

```
python3 username\\\\\\\\\\\\\\\_checker.py
```

\---

## usage

when you run the tool it asks you step by step:

```
\\\\\\\\\\\\\\\[ Platform ]     pick which platform to check
\\\\\\\\\\\\\\\[ Input Mode ]   generate automatically or load from .txt file
\\\\\\\\\\\\\\\[ Length ]       3, 4, 5 or 6 letters
\\\\\\\\\\\\\\\[ Charset ]      letters / letters+numbers / letters+underscore / all
\\\\\\\\\\\\\\\[ Speed ]        normal / fast / turbo
```

press `ENTER` to start — hits get printed live and saved automatically.
press `Ctrl+C` at any time to stop, results already found are kept.
press `y` when prompted to run again with new settings.

**output files:**

```
available\\\\\\\\\\\\\\\_roblox.txt
available\\\\\\\\\\\\\\\_minecraft.txt
available\\\\\\\\\\\\\\\_tiktok.txt
available\\\\\\\\\\\\\\\_youtube.txt
available\\\\\\\\\\\\\\\_twitch.txt
available\\\\\\\\\\\\\\\_github.txt
available\\\\\\\\\\\\\\\_twitter.txt
available\\\\\\\\\\\\\\\_gunslol.txt
```

\---

## custom wordlist

you can load your own `.txt` file instead of generating names automatically:

1. put your `.txt` file in the same folder as `username\\\\\\\\\\\\\\\_checker.py`
2. run the script and choose `\\\\\\\\\\\\\\\[2] Load from custom .txt file`
3. type the filename when asked (e.g. `usernames.txt`)

format — one username per line, lines starting with `#` are ignored:

```
# my custom list
krova
zyx4
nexon
```

\---

## tips

* for **GitHub** and **Twitter** use normal speed — they rate limit hard
* for **Roblox** 3-letter names use letters+numbers, pure letters are mostly gone
* results are random every run so everyone checks different names
* if you get lots of `\\\\\\\\\\\\\\\[ERR]` try lowering the thread count
* on Linux if install fails add `--break-system-packages` to the pip command

\---

## changelog

# v1.2 — Update Log

## bug fixes

* fixed false positives — usernames were being reported as available when they were actually taken
* removed guns.lol (unreliable platform — too many false positives, no reliable detection method)

## platform checker rewrites

* **TikTok** — completely rewritten

  * old method used page length and vague keyword matching — caused false positives
  * now only returns available if `"statusCode":10202` is found in page JSON
  * now only returns taken if exact `"uniqueId":"name"` match is found
  * added bad response detection (captcha, cloudflare, blocked pages)
* **Twitter / X** — rewritten

  * old method used loose text matching — anything containing the name triggered false negative
  * now parses `screen\\\\\\\\\\\\\\\_name` field exactly from syndication API response
  * only returns available on hard HTTP 404
* **YouTube** — improved

  * now verifies oEmbed response contains `author\\\\\\\\\\\\\\\_name` or `title` before marking taken
  * prevents false negatives from malformed 200 responses
* **Twitch** — improved

  * now verifies `login` field exactly matches queried name before marking taken
  * previously marked taken if any `login` key existed in response
* **GitHub** — improved

  * now verifies returned `login` exactly matches queried name
  * prevents edge cases with redirected or renamed accounts
* **Minecraft** — improved

  * added name format validation (only a-z, 0-9, \_ allowed)
  * now verifies `name` field in response matches before marking taken

## new

* added `bad\\\\\\\\\\\\\\\_response()` helper that detects captcha pages, cloudflare blocks, and empty responses
* all checkers now return `None` for any uncertainty instead of guessing
* uncertain results shown as `\\\\\\\\\\\\\\\[ERR]` in terminal, never reported as available

**v1.1**

* full Linux and macOS compatibility
* custom .txt wordlist support
* live estimated time remaining
* run again option after finishing
* 3-letter username support
* underscore bug fixed (max 1 per name)
* stability improvements

**v1.0**

* initial release

\---

## discord

<div align="center">

[!\[Discord Server](https://img.shields.io/badge/Join%25252520the%25252520Discord-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/DZMNzW3xCx)

join for help, updates and to share your finds

</div>

\---

## credits

<div align="center">

made by ‎Duff

</div>

