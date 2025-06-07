import os
import tempfile
import shutil
import pytest
from mitmproxy import http
from types import SimpleNamespace

# Import the mitmproxy script you want to test
import mitm_script

@pytest.fixture(autouse=True)
def setup_test_logs(monkeypatch):
    # Create a temporary directory and empty log files
    temp_dir = tempfile.mkdtemp()
    banned = os.path.join(temp_dir, "banned_words.log")
    ads = os.path.join(temp_dir, "blocked_ads.log")
    content = os.path.join(temp_dir, "blocked_websites.log")
    rules = os.path.join(temp_dir, "ad_rules.log")

    # Write a simple adblock rule
    with open(rules, "w", encoding="utf-8") as f:
        f.write("||ads.example.com^")

    # Write a sample banned word
    with open(banned, "w", encoding="utf-8") as f:
        f.write("badword\n")

    # Override paths in the module
    monkeypatch.setattr(mitm_script, "BANNED_WORDS_FILE", banned)
    monkeypatch.setattr(mitm_script, "LOG_FILE_ADS", ads)
    monkeypatch.setattr(mitm_script, "LOG_FILE_CONTENT", content)
    monkeypatch.setattr(mitm_script, "LOG_AD_RULES", rules)

    # Reinitialize adblock rules
    with open(rules, "r", encoding="utf-8") as f:
        raw_rules = [line.strip() for line in f if line and not line.startswith("!")]
    mitm_script.rules = mitm_script.AdblockRules(raw_rules)

    yield {
        "banned": banned,
        "ads": ads,
        "content": content
    }

    shutil.rmtree(temp_dir)

def create_flow(url, content_type="text/html", content_body=""):
    request = http.Request.make("GET", url)
    response = http.Response.make(200, content_body.encode("utf-8"), {"Content-Type": content_type})
    return SimpleNamespace(request=request, response=response)

def test_ad_blocking(setup_test_logs):
    flow = create_flow("http://ads.example.com/banner.js")
    flow.response = None
    mitm_script.request(flow)
    with open(setup_test_logs["ads"], "r", encoding="utf-8") as f:
        assert "ads.example.com" in f.read()
    assert flow.response.status_code == 403

def test_content_blocking(setup_test_logs):
    flow = create_flow("http://example.com", content_body="This page contains badword and should be blocked.")
    mitm_script.response(flow)
    with open(setup_test_logs["content"], "r", encoding="utf-8") as f:
        assert "badword" in f.read()
    assert flow.response.status_code == 403
