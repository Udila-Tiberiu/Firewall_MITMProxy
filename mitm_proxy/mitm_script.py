from mitmproxy import http
from adblockparser import AdblockRules
import fnmatch
import os
import re

AD_PATTERNS = [
    "*://*.doubleclick.net/*",
    "*://*.googlesyndication.com/*",
    "*://*.googletagservices.com/*",
    "*://*.googleleadservices.com/*",
    "*://*.googleadservices.com/*",
    "*://*.google-analytics.com/*",
    "*://*.zedo.com/*",
    "*://*.adbrite.com/*",
    "*://*.adbureau.net/*",
    "*://*.carbonads.net/*",
    "*://*.cdn.carbonads.net/*",
    "*://*.cdn.carbonads.com/*",
    "*://*.cdn.doubleclick.net/*",
    "*://*.cdn.googleadservices.com/*",
    "*://*.cdn.googletagservices.com/*",
    "*://*.cdn.zedo.com/*"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANNED_WORDS_FILE = os.path.join(BASE_DIR, "../banned_words.log")
LOG_FILE_ADS = os.path.join(BASE_DIR, "../blocked_ads.log")
LOG_FILE_CONTENT = os.path.join(BASE_DIR, "../blocked_websites.log")
LOG_AD_RULES = os.path.join(BASE_DIR, "../ad_rules.log")

def load_banned_keywords():
    if os.path.exists(BANNED_WORDS_FILE):
        with open(BANNED_WORDS_FILE, "r", encoding="utf-8") as file:
            return [line.strip().lower() for line in file if line.strip()]
    return []

def matches_ad_pattern(url: str) -> bool:
    for pattern in AD_PATTERNS:
        wildcard_pattern = pattern.replace("*://", "*")
        if fnmatch.fnmatch(url, wildcard_pattern):
            return True
    return False

def find_blocked_keyword(content: str) -> str | None:
    blocked_keywords = load_banned_keywords()
    lowered = content.lower()
    for word in blocked_keywords:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, lowered):
            return word
    return None

with open(LOG_AD_RULES, "r", encoding="utf-8") as f:
    raw_rules = [line.strip() for line in f if line and not line.startswith("!")]
rules = AdblockRules(raw_rules)

def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    if rules.should_block(url, {"domain": flow.request.host}) or matches_ad_pattern(url):
        with open(LOG_FILE_ADS, "a", encoding="utf-8") as log_file:
            log_file.write(url + "\n")
        flow.response = http.Response.make(
            403,
            b"Blocked by Adblock rules",
            {"Content-Type": "text/plain"}
        )

def response(flow: http.HTTPFlow) -> None:
    if flow.response and "text" in flow.response.headers.get("Content-Type", ""):
        try:
            content = flow.response.get_text()
            matched_word = find_blocked_keyword(content)
            if matched_word:
                url = flow.request.url
                with open(LOG_FILE_CONTENT, "a", encoding="utf-8") as log_file:
                    log_file.write(f"{matched_word} {url}\n")
                flow.response = http.Response.make(
                    403,
                    b"Blocked by mitmproxy content filter",
                    {"Content-Type": "text/plain"}
                )
        except Exception:
            pass
