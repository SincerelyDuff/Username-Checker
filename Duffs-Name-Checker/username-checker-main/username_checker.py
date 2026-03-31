#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import random
import threading
import string
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

# settings
THREADS = 25
DELAY   = 0.05
RETRIES = 3
VERSION = "1.2"
AUTHOR  = "Duff"

outdir  = os.path.dirname(os.path.abspath(__file__))
UA      = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

_lock   = threading.Lock()
_checked = 0
_found   = 0
_errors  = 0
_total   = 0
_start   = 0.0
_tlocal  = threading.local()

letters = list(string.ascii_lowercase)
digits  = list(string.digits)
vowels  = list("aeiou")
cons    = list("bcdfghjklmnprstvwxyz")

cool_starts = [
    "kr","dr","br","gr","tr","pr","bl","cl","fl","gl","sl",
    "sk","sp","st","sw","zr","vr","sh","ch","nx","vx","zx",
]

pat3 = ["CVC","CVV","VCV","VCC","CCV","VVC"]
pat4 = ["CVCC","CVCV","CCVC","VCVC","CVVC","VCCV","CCVV","VVCV"]
pat5 = ["CVCCV","CVCVC","CCVCV","VCVCV","CVCVV","CVVCV","CCVCC","VCCVC"]
pat6 = ["CVCCVC","CVCVCV","CVVCVC","CCVCVC","VCVCVC","CVCVVC","CVCCVV"]

PLATFORMS = {
    "1": {"name": "Roblox",      "file": "available_roblox.txt",   "check": "roblox",    "min_len": 3, "note": "official API"},
    "2": {"name": "Minecraft",   "file": "available_minecraft.txt","check": "minecraft", "min_len": 3, "note": "official API"},
    "3": {"name": "TikTok",      "file": "available_tiktok.txt",   "check": "tiktok",    "min_len": 4, "note": "content check"},
    "4": {"name": "YouTube",     "file": "available_youtube.txt",  "check": "youtube",   "min_len": 4, "note": "oEmbed API"},
    "5": {"name": "Twitch",      "file": "available_twitch.txt",   "check": "twitch",    "min_len": 4, "note": "GQL API"},
    "6": {"name": "Twitter / X", "file": "available_twitter.txt",  "check": "twitter",   "min_len": 4, "note": "use normal speed"},
}


# ── colors ─────────────────────────────────────────────────────
def col(txt, clr):
    if not HAS_COLOR:
        return str(txt)
    m = {
        "red":    Fore.RED,
        "green":  Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan":   Fore.CYAN,
        "white":  Fore.WHITE,
        "gray":   Fore.WHITE + Style.DIM,
    }
    return m.get(clr, "") + str(txt) + Style.RESET_ALL


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    clear()
    print()
    print(col("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠐⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⣍⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣶⣶⣄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣄⠀⠀⠀⠀⠀⣀⡀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣷⠀⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⡟⠀⠹⣿⣿⣿⣦⠀⢀⣶⣿⣿⣿⣷⡀⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⠁⠀⣀⣈⠻⣿⣿⣷⣿⣿⣿⣿⣿⡿⠁⠹⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡏⢠⣾⣿⣿⣷⣜⢿⣿⣿⣦⠀⠀⠀⠀⢀⣀⣈⡙⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣧⣝⣛⣡⣶⣶⣾⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠛⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠈⠀⠀
⠀⢀⣤⣤⣤⣤⣤⣼⣿⣿⣿⣿⡇⠀⢹⣿⣿⣿⣿⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢠⣼⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⢀⣿⣿⣿⣤⣤⣄⣀⣀⣀⡀⠀⠀⠀⠀⠁⠀⠀⠈⠀⠀⠀⠀
⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""", "cyan"))
    print()
    print(col(f"  Multi-Platform Username Checker v{VERSION}  |  by {AUTHOR}", "gray"))
    print(col("  " + "-" * 55, "gray"))
    print()


def hdr(title):
    print(col(f"\n  [ {title} ]", "cyan"))
    print(col("  " + "-" * 44, "gray"))


def ask(txt):
    try:
        return input(col("  > ", "cyan") + col(txt + " ", "white")).strip()
    except EOFError:
        return ""


def opt(k, lbl, note=""):
    line = col(f"  [{k}]", "yellow") + col(f"  {lbl}", "white")
    if note:
        line += col(f"  ({note})", "gray")
    print(line)


# ── status line ────────────────────────────────────────────────
def draw(name, result):
    pct = int((_checked / _total) * 100) if _total > 0 else 0
    bar = "#" * (pct // 5) + "-" * (20 - pct // 5)

    elapsed = time.time() - _start
    if _checked > 0 and elapsed > 0:
        rem = (_total - _checked) / (_checked / elapsed)
        if rem >= 3600:
            eta = f"{int(rem//3600)}h{int((rem%3600)//60)}m"
        elif rem >= 60:
            eta = f"{int(rem//60)}m{int(rem%60)}s"
        else:
            eta = f"{int(rem)}s"
    else:
        eta = "--"

    if result is True:
        tag = col("  [HIT] ", "green")
    elif result is False:
        tag = col("  [----]", "gray")
    else:
        tag = col("  [ERR] ", "yellow")

    line = (
        f"\r{tag} "
        + col(name.ljust(14), "white")
        + col(f" [{bar}] {pct:3}%", "gray")
        + col(f"  {_checked}/{_total}", "gray")
        + col(f"  hits:{_found}", "green")
        + col(f"  eta:{eta}  ", "gray")
    )
    try:
        sys.stdout.write(line)
        sys.stdout.flush()
    except Exception:
        pass


# ── session ────────────────────────────────────────────────────
def sess():
    if not hasattr(_tlocal, "s"):
        s = requests.Session()
        s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
        adp = HTTPAdapter(
            pool_connections=THREADS,
            pool_maxsize=THREADS,
            max_retries=Retry(total=2, backoff_factor=0.3)
        )
        s.mount("https://", adp)
        _tlocal.s = s
    return _tlocal.s


# ── bad response detector ──────────────────────────────────────
def bad_response(text):
    # detect captcha, blocked, or empty pages
    # return True = response is useless, treat as None
    if not text or len(text) < 500:
        return True
    t = text.lower()
    return any(s in t for s in [
        "captcha",
        "verify you are human",
        "access denied",
        "cf-browser-verification",
        "enable javascript",
        "ddos-guard",
    ])


# ── platform checkers ──────────────────────────────────────────
# True  = 100% confirmed available
# False = confirmed taken
# None  = uncertain, never guess

def check_roblox(name):
    # Official Roblox validation API
    # code 0 = available, code 1 = taken
    url = "https://auth.roblox.com/v1/usernames/validate"
    p = {
        "request.username": name,
        "request.birthday": "2000-01-01",
        "request.context": "signup"
    }
    for attempt in range(RETRIES):
        try:
            r = sess().get(url, params=p, timeout=6)
            if r.status_code == 200:
                code = r.json().get("code", -1)
                if code == 0:
                    return True
                elif code == 1:
                    return False
                else:
                    return None
            elif r.status_code == 429:
                time.sleep(5 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(1)
    return None


def check_minecraft(name):
    # Official Mojang API
    # 404 = available, 200 = taken
    # validate name matches response to avoid edge cases
    if not all(c in string.ascii_letters + string.digits + "_" for c in name):
        return None
    for attempt in range(RETRIES):
        try:
            r = sess().get(f"https://api.mojang.com/users/profiles/minecraft/{name}", timeout=6)
            if r.status_code == 404:
                return True
            elif r.status_code == 200:
                data = r.json()
                if data.get("name", "").lower() == name.lower():
                    return False
                return None
            elif r.status_code == 429:
                time.sleep(5 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(1)
    return None


def check_tiktok(name):
    # TikTok SPA — always returns 200 even for missing users
    # TAKEN signal:    "uniqueId":"name" in page JSON
    # AVAILABLE signal: "statusCode":10202 in page JSON
    # Everything else: return None — never guess
    h = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.tiktok.com/",
    }
    for attempt in range(RETRIES):
        try:
            r = sess().get(
                f"https://www.tiktok.com/@{name}",
                headers=h, timeout=12, allow_redirects=True
            )
            if r.status_code == 429:
                time.sleep(8 * (attempt + 1))
                continue
            if r.status_code == 404:
                return True
            if r.status_code != 200:
                return None
            if bad_response(r.text):
                return None

            t = r.text
            # exact uniqueId match = taken
            if f'"uniqueId":"{name}"' in t or f'"uniqueId":"{name.lower()}"' in t:
                return False
            # statusCode 10202 = user not found = available
            if '"statusCode":10202' in t:
                return True
            # uncertain
            return None
        except Exception:
            time.sleep(2)
    return None


def check_youtube(name):
    # YouTube oEmbed API
    # 200 + author_name = channel exists = taken
    # 400 or 404 = handle does not exist = available
    # anything else = uncertain
    # NOTE: YouTube returns 400 (not 404) for missing handles
    for attempt in range(RETRIES):
        try:
            r = sess().get(
                "https://www.youtube.com/oembed",
                params={"url": f"https://www.youtube.com/@{name}", "format": "json"},
                timeout=8,
            )
            if r.status_code in (400, 404):
                # double check it's not a bad/malformed request on our end
                # only mark available if the name is valid format
                if " " in name or len(name) < 3:
                    return None
                return True
            elif r.status_code == 200:
                try:
                    data = r.json()
                    if data.get("author_name") and data["author_name"].strip():
                        return False
                except Exception:
                    pass
                return None
            elif r.status_code == 429:
                time.sleep(8 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(2)
    return None


def check_twitch(name):
    # Twitch public GQL API
    # UserDoesNotExist = available, login matches = taken
    h = {
        "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "Content-Type": "application/json",
    }
    body = [{
        "operationName": "ChannelShell",
        "variables": {"login": name},
        "extensions": {"persistedQuery": {
            "version": 1,
            "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
        }}
    }]
    for attempt in range(RETRIES):
        try:
            r = sess().post("https://gql.twitch.tv/gql", json=body, headers=h, timeout=8)
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            if r.status_code != 200:
                return None
            data = r.json()
            if not isinstance(data, list) or not data:
                return None
            user = data[0].get("data", {}).get("userOrError")
            if user is None:
                return None
            if user.get("__typename") == "UserDoesNotExist":
                return True
            if user.get("login", "").lower() == name.lower():
                return False
            return None
        except Exception:
            time.sleep(1)
    return None


def check_github(name):
    # GitHub public REST API
    # 404 = available, 200 with matching login = taken
    for attempt in range(RETRIES):
        try:
            r = sess().get(f"https://api.github.com/users/{name}", timeout=6)
            if r.status_code == 404:
                return True
            elif r.status_code == 200:
                try:
                    data = r.json()
                    if data.get("login", "").lower() == name.lower():
                        return False
                except Exception:
                    pass
                return None
            elif r.status_code in [429, 403]:
                time.sleep(10 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(1)
    return None


def check_twitter(name):
    # Twitter syndication API
    # 404 = available
    # screen_name exact match in response = taken
    # anything else = None
    for attempt in range(RETRIES):
        try:
            r = sess().get(
                f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{name}",
                timeout=10, allow_redirects=True,
            )
            if r.status_code == 404:
                return True
            elif r.status_code == 200:
                if bad_response(r.text):
                    return None
                marker = '"screen_name":"'
                idx = r.text.find(marker)
                if idx != -1:
                    start = idx + len(marker)
                    end = r.text.find('"', start)
                    sn = r.text[start:end]
                    if sn.lower() == name.lower():
                        return False
                return None
            elif r.status_code == 429:
                time.sleep(10 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(2)
    return None


CHECKERS = {
    "roblox":    check_roblox,
    "minecraft": check_minecraft,
    "tiktok":    check_tiktok,
    "youtube":   check_youtube,
    "twitch":    check_twitch,
    "twitter":   check_twitter,
}


# ── worker ─────────────────────────────────────────────────────
def worker(name, hits, outfile, fn):
    global _checked, _found, _errors

    if not name or " " in name:
        with _lock:
            _errors += 1
        return

    time.sleep(DELAY + random.uniform(0, 0.08))
    result = fn(name)

    with _lock:
        _checked += 1

        if result is True:
            _found += 1
            hits.append(name)
            try:
                with open(outfile, "a", encoding="utf-8") as f:
                    f.write(name + "\n")
            except Exception:
                pass
            sys.stdout.write("\r" + " " * 90 + "\r")
            sys.stdout.flush()
            print(col(f"  [AVAILABLE]  {name}", "green") +
                  col(f"  [{datetime.now().strftime('%H:%M:%S')}]", "gray"))

        elif result is False:
            draw(name, False)

        else:
            _errors += 1
            draw(name, None)


# ── name generators ────────────────────────────────────────────
def make_letter_names(length, count=80000):
    names = set()
    pats = pat3 if length == 3 else pat4 if length == 4 else pat5 if length == 5 else pat6
    for pat in pats:
        for _ in range(3000):
            n = "".join(random.choice(vowels if c == "V" else cons) for c in pat)
            if len(n) == length:
                names.add(n)
    for start in cool_starts:
        if len(start) >= length:
            continue
        for _ in range(400):
            fill, was_v = "", start[-1] in vowels
            for _ in range(length - len(start)):
                ch = random.choice(cons) if was_v else (
                    random.choice(vowels) if random.random() > 0.3 else random.choice(cons))
                fill += ch
                was_v = ch in vowels
            n = start + fill
            if len(n) == length:
                names.add(n)
    while len(names) < count:
        n, sc = "", random.random() > 0.3
        for i in range(length):
            n += random.choice(cons if (i % 2 == 0) == sc else vowels)
        if n[0].isalpha():
            names.add(n)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_num_names(length, count=80000):
    names = set()
    while len(names) < count:
        n = [random.choice(letters)]
        for _ in range(length - 1):
            n.append(random.choice(letters) if random.random() < 0.65 else random.choice(digits))
        names.add("".join(n))
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_underscore_names(length, count=80000):
    names = set()
    while len(names) < count:
        n, used = [random.choice(letters)], False
        for i in range(length - 1):
            if random.random() < 0.75 or used:
                n.append(random.choice(letters))
            elif n[-1] != "_" and i != length - 2:
                n.append("_")
                used = True
            else:
                n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_all(length, count=80000):
    names = set()
    while len(names) < count:
        n, used = [random.choice(letters)], False
        for i in range(length - 1):
            r = random.random()
            if r < 0.55:
                n.append(random.choice(letters))
            elif r < 0.85:
                n.append(random.choice(digits))
            elif not used and n[-1] != "_" and i != length - 2:
                n.append("_")
                used = True
            else:
                n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]


# ── main ───────────────────────────────────────────────────────
def run():
    global _checked, _found, _errors, _total, _start

    while True:
        banner()

        # platform
        hdr("Platform")
        for k, v in PLATFORMS.items():
            opt(k, v["name"], v["note"])
        pc = ask("Choose platform:")
        while pc not in PLATFORMS:
            print(col(f"  enter 1-{len(PLATFORMS)}", "red"))
            pc = ask("Choose platform:")
        platform = PLATFORMS[pc]

        # input mode
        hdr("Input Mode")
        opt("1", "Generate usernames automatically")
        opt("2", "Load from custom .txt file")
        mode = ask("Choose mode:")
        while mode not in ["1", "2"]:
            print(col("  enter 1 or 2", "red"))
            mode = ask("Choose mode:")

        custom_txt, names, length, cc = False, [], 0, "custom"
        fname = ""

        if mode == "2":
            hdr("Load File")
            print(col("  put your .txt file in the same folder as this script", "gray"))
            print(col("  one username per line", "gray"))
            fname = ask("Filename (e.g. usernames.txt):")
            fpath = fname if os.path.isabs(fname) else os.path.join(outdir, fname)
            if not os.path.exists(fpath):
                print(col("  file not found", "red"))
                input(col("\n  press ENTER to try again\n", "yellow"))
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                names = [
                    l.strip() for l in f
                    if l.strip()
                    and not l.startswith("#")
                    and " " not in l.strip()
                ]
            random.shuffle(names)
            custom_txt = True
            print(col(f"  loaded {len(names):,} usernames", "green"))
        else:
            hdr("Length")
            avail = [l for l in [3, 4, 5, 6] if l >= platform["min_len"]]
            for i, l in enumerate(avail, 1):
                opt(str(i), f"{l} letters")
            lc = ask("Choose length:")
            while not lc.isdigit() or int(lc) not in range(1, len(avail) + 1):
                print(col(f"  enter 1-{len(avail)}", "red"))
                lc = ask("Choose length:")
            length = avail[int(lc) - 1]

            hdr("Character Set")
            opt("1", "Letters only          (a-z)")
            opt("2", "Letters + numbers     (a-z, 0-9)")
            opt("3", "Letters + underscore  (a-z, _)")
            opt("4", "All                   (a-z, 0-9, _)")
            cc = ask("Choose charset:")
            while cc not in ["1", "2", "3", "4"]:
                print(col("  enter 1-4", "red"))
                cc = ask("Choose charset:")

        hdr("Speed")
        if platform["check"] in ["github", "twitter"]:
            opt("1", "Normal   (5 threads)  -- recommended")
            opt("2", "Fast     (10 threads)")
            opt("3", "Turbo    (20 threads)")
            threads = {"1": 5, "2": 10, "3": 20}.get(ask("Choose speed:"), 5)
        else:
            opt("1", "Normal   (15 threads)")
            opt("2", "Fast     (25 threads)")
            opt("3", "Turbo    (50 threads)")
            threads = {"1": 15, "2": 25, "3": 50}.get(ask("Choose speed:"), 25)

        if not custom_txt:
            hdr("Generating")
            print(col("  generating, please wait...", "gray"))
            if cc == "1":
                names = make_letter_names(length)
            elif cc == "2":
                names = make_num_names(length)
            elif cc == "3":
                names = make_underscore_names(length)
            else:
                names = make_all(length)
            random.shuffle(names)
            print(col(f"  {len(names):,} usernames ready", "green"))

        _total  = len(names)
        outfile = os.path.join(outdir, platform["file"])
        clabels = {
            "1": "letters only", "2": "letters+numbers",
            "3": "letters+underscore", "4": "all", "custom": "custom file"
        }

        hdr("Summary")
        print(col("  Platform   ", "gray") + col(platform["name"], "white"))
        if custom_txt:
            print(col("  Source     ", "gray") + col(fname, "white"))
        else:
            print(col("  Length     ", "gray") + col(f"{length}-letter", "white"))
            print(col("  Charset    ", "gray") + col(clabels[cc], "white"))
        print(col("  Threads    ", "gray") + col(str(threads), "white"))
        print(col("  Usernames  ", "gray") + col(f"{_total:,}", "white"))
        print(col("  Sample     ", "gray") + col(", ".join(names[:6]), "white"))
        print()

        try:
            input(col("  Press ENTER to start  |  Ctrl+C to stop\n", "yellow"))
        except KeyboardInterrupt:
            print()
            break

        _checked = _found = _errors = 0
        hits     = []
        fn       = CHECKERS[platform["check"]]
        _start   = time.time()

        try:
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(f"# {platform['name']} available usernames\n")
                f.write(f"# by {AUTHOR}  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        except Exception as e:
            print(col(f"  warning: could not create output file ({e})", "yellow"))

        hdr("Checking")
        print(col("  [HIT] = available   [----] = taken   [ERR] = uncertain\n", "gray"))

        t0 = time.time()
        try:
            with ThreadPoolExecutor(max_workers=threads) as ex:
                futs = {ex.submit(worker, u, hits, outfile, fn): u for u in names}
                for ft in as_completed(futs):
                    try:
                        ft.result()
                    except Exception:
                        pass
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            print(col("\n  stopped.", "red"))

        elapsed = time.time() - t0
        rate    = _checked / elapsed if elapsed > 0 else 0

        sys.stdout.write("\n")
        hdr("Results")
        print(col("  Platform  ", "gray") + col(platform["name"], "white"))
        print(col("  Checked   ", "gray") + col(f"{_checked:,}", "white"))
        print(col("  Time      ", "gray") + col(f"{elapsed:.1f}s  ({rate:.1f}/sec)", "white"))
        print(col("  Found     ", "gray") + col(str(len(hits)), "green" if hits else "white"))
        print(col("  Uncertain ", "gray") + col(str(_errors), "yellow" if _errors else "white"))

        if hits:
            print()
            print(col("  available usernames:", "green"))
            for h in hits:
                print(col(f"    -> {h}", "green"))

        print()
        print(col("  " + "-" * 45, "gray"))
        print(col(f"  checker by {AUTHOR}", "cyan"))
        print()

        try:
            again = ask("run again? [y/n]").lower()
        except KeyboardInterrupt:
            break

        if again != "y":
            break

    print(col("\n  bye!\n", "cyan"))


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(col("\n\n  bye!\n", "cyan"))
        sys.exit(0)