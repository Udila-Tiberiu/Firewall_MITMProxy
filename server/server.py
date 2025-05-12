from flask import Flask, jsonify, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANNED_WORDS_FILE = os.path.join(BASE_DIR, "../banned_words.log")
LOG_FILE_ADS = os.path.join(BASE_DIR, "../blocked_ads.log")
LOG_FILE_CONTENT = os.path.join(BASE_DIR, "../blocked_websites.log")

def read_log(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    return []

@app.route("/logs/ads", methods=["GET"])
def get_ads_log():
    return jsonify(read_log(LOG_FILE_ADS))

@app.route("/logs/content", methods=["GET"])
def get_content_log():
    return jsonify(read_log(LOG_FILE_CONTENT))

@app.route("/logs/banned_words", methods=["GET"])
def get_banned_words():
    if os.path.exists(BANNED_WORDS_FILE):
        with open(BANNED_WORDS_FILE, "r", encoding="utf-8") as file:
            return jsonify([line.strip() for line in file if line.strip()])
    return jsonify([])

@app.route("/logs/clear/<log_type>", methods=["POST"])
def clear_log(log_type):
    file_map = {
        "ads": LOG_FILE_ADS,
        "content": LOG_FILE_CONTENT
    }
    file_path = file_map.get(log_type)
    if file_path and os.path.exists(file_path):
        open(file_path, "w").close()
        return jsonify({"status": "cleared"}), 200
    return jsonify({"error": "Invalid log type"}), 400

@app.route("/logs/banned_words", methods=["POST"])
def add_banned_word():
    word = request.json.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Avoid duplicates
    existing = read_log(BANNED_WORDS_FILE)
    if word not in existing:
        with open(BANNED_WORDS_FILE, "a", encoding="utf-8") as file:
            file.write(word + "\n")

    return jsonify({"status": "added", "word": word})


@app.route("/logs/banned_words", methods=["DELETE"])
def delete_banned_word():
    word = request.json.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "No word provided"}), 400

    existing = read_log(BANNED_WORDS_FILE)
    if word in existing:
        updated = [w for w in existing if w != word]
        with open(BANNED_WORDS_FILE, "w", encoding="utf-8") as file:
            for w in updated:
                file.write(w + "\n")

    return jsonify({"status": "deleted", "word": word})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
