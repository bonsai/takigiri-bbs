import json
import os
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bbs.json")
JST = timezone(timedelta(hours=9))


def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def now_str():
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M")


def make_id():
    return datetime.now(JST).strftime("%Y%m%d%H%M%S%f")


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = load_posts()
    posts.sort(key=lambda p: p.get("created_at", ""), reverse=True)
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("comment"):
        return jsonify({"error": "名前とコメントは必須です"}), 400

    post = {
        "id": make_id(),
        "name": data["name"].strip(),
        "comment": data["comment"].strip(),
        "created_at": now_str(),
        "reply_to": data.get("reply_to", None),
        "lat": data.get("lat", None),
        "lng": data.get("lng", None),
    }

    posts = load_posts()
    posts.append(post)
    save_posts(posts)
    return jsonify(post), 201


@app.route("/api/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
