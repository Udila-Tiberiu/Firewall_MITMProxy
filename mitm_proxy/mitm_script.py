from mitmproxy import http
import fnmatch

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

# Words to block if found in page content
BLOCKED_KEYWORDS = [
    "gambling",
]

LOG_FILE_ADS = "blocked_ads.log"
LOG_FILE_CONTENT = "blocked_websites.log"

def matches_ad_pattern(url: str) -> bool:
    for pattern in AD_PATTERNS:
        wildcard_pattern = pattern.replace("*://", "*")
        if fnmatch.fnmatch(url, wildcard_pattern):
            return True
    return False

def contains_blocked_keywords(content: str) -> bool:
    lowered = content.lower()
    return any(word in lowered for word in BLOCKED_KEYWORDS)

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
            pass  # Some content might not decode properly; skip those
