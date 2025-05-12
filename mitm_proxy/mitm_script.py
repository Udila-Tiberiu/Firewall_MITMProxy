from mitmproxy import http
import fnmatch
import os

# Ad URL patterns to block
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

def contains_blocked_keywords(content: str) -> bool:
    blocked_keywords = load_banned_keywords()
    lowered = content.lower()
    return any(word in lowered for word in blocked_keywords)

def request(flow: http.HTTPFlow) -> None:
    url = flow.request.url
    if matches_ad_pattern(url):
        with open(LOG_FILE_ADS, "a", encoding="utf-8") as log_file:
            log_file.write(url + "\n")
        flow.response = http.Response.make(
            403,
            b"Blocked by mitmproxy ad blocker",
            {"Content-Type": "text/plain"}
        )

def response(flow: http.HTTPFlow) -> None:
    if flow.response and "text" in flow.response.headers.get("Content-Type", ""):
        try:
            content = flow.response.get_text()
            if contains_blocked_keywords(content):
                url = flow.request.url
                with open(LOG_FILE_CONTENT, "a", encoding="utf-8") as log_file:
                    log_file.write(url + "\n")
                flow.response = http.Response.make(
                    403,
                    b"Blocked by mitmproxy content filter",
                    {"Content-Type": "text/plain"}
                )
        except Exception:
            pass
