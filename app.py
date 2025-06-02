## app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    print("Webhook received:", event)

    record = {}

    if event == "push":
        print("Handling push event")
        record = {
            "action": "push",
            "author": payload["pusher"]["name"],
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"]
        }

    elif event == "pull_request":
        print("Handling pull_request event")
        pr = payload["pull_request"]
        action = payload["action"]

        if action == "opened":
            record = {
                "action": "pull_request",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }

        elif action == "closed" and pr.get("merged"):
            record = {
                "action": "merge",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"]
            }

    if record:
        print("Inserting into MongoDB:", record)
        db.events.insert_one(record)

    return jsonify({"message": "Webhook received"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(db.events.find().sort("timestamp", -1))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)