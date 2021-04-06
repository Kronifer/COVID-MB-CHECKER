from flask import Flask, render_template, request, jsonify
import pymongo
import os

client = pymongo.MongoClient(
    os.getenv("MKEY")
)

db = client.COVID_TRACKER

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template("main.html")

@app.route("/submit", methods=["GET"])
def submit():
    try:
        email = request.args.get("email")
    except:
        return "No email submitted."
    collection = db.Emails
    data = collection.find_one({}, {"_id": 0})
    rawlist = data.get("emails")
    rawlist.append(email)
    collection.find_one_and_update({},
    {"$set":
            {"emails": rawlist}}, upsert=True)
    return "Email added!"
    