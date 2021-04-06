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
    email = request.args.get("email")
    print(type(email))
    if email is None:
        return "No email submitted."
    elif "@" not in email:
        return "Invalid email."
    collection = db.Emails
    data = collection.find_one({}, {"_id": 0})
    rawlist = data.get("emails")
    rawlist.append(email)
    collection.find_one_and_update({},
    {"$set":
            {"emails": rawlist}}, upsert=True)
    return "Email added! If there has already been a news release today, you will get an email tomorrow."

@app.route("/unregister", methods=["GET"])
def unregister():
    return render_template("unregister.html")

@app.route("/unregisterprocess", methods=["GET"])
def unregisterprocess():
    email = request.args.get("email")
    if email is None:
        return "No email submitted."
    elif "@" not in email:
        return "Invalid email."
    collection = db.Emails
    data = collection.find_one({}, {"_id": 0})
    rawlist = data.get("emails")
    rawlist.remove(email)
    collection.find_one_and_update({},
    {"$set":
            {"emails": rawlist}}, upsert=True)
    return "Unregistered from COVID checker."

    
