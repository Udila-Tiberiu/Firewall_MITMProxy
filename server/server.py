from flask import Flask, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

LOG_FILE_ADS = "blocked_ads.log"
LOG_FILE_CONTENT = "blocked_websites.log"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
