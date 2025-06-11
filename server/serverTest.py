import os
import pytest
import server
from server import app

@pytest.fixture
def client(tmp_path):
    server.BANNED_WORDS_FILE = tmp_path / "banned_words.log"
    server.LOG_FILE_ADS = tmp_path / "blocked_ads.log"
    server.LOG_FILE_CONTENT = tmp_path / "blocked_websites.log"

    for file in [server.BANNED_WORDS_FILE, server.LOG_FILE_ADS, server.LOG_FILE_CONTENT]:
        file.write_text("")

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_empty_logs(client):
    assert client.get("/logs/ads").get_json() == []
    assert client.get("/logs/content").get_json() == []
    assert client.get("/logs/banned_words").get_json() == []

def test_add_and_get_banned_word(client):
    rv = client.post("/logs/banned_words", json={"word": "SPAM"})
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "added", "word": "spam"}

    rv = client.get("/logs/banned_words")
    assert "spam" in rv.get_json()

    rv = client.post("/logs/banned_words", json={"word": "spam"})
    assert rv.status_code == 200

    words = client.get("/logs/banned_words").get_json()
    assert words.count("spam") == 1

def test_delete_banned_word(client):
    client.post("/logs/banned_words", json={"word": "spam"})
    rv = client.delete("/logs/banned_words", json={"word": "spam"})
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "deleted", "word": "spam"}

    rv = client.get("/logs/banned_words")
    assert "spam" not in rv.get_json()

def test_clear_log(client):
    server.LOG_FILE_ADS.write_text("http://ad.com\n")
    assert client.get("/logs/ads").get_json() == ["http://ad.com"]

    rv = client.post("/logs/clear/ads")
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "cleared"}

    assert client.get("/logs/ads").get_json() == []

    rv = client.post("/logs/clear/invalid")
    assert rv.status_code == 400

def test_get_content_log(client):
    lines = [
        "ads http://example.com/ad",
        "spam http://example.com/spam"
    ]
    server.LOG_FILE_CONTENT.write_text("\n".join(lines) + "\n")

    rv = client.get("/logs/content")
    assert rv.status_code == 200
    data = rv.get_json()

    assert {"word": "ads", "url": "http://example.com/ad"} in data
    assert {"word": "spam", "url": "http://example.com/spam"} in data
