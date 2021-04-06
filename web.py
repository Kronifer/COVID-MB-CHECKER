from flask import Flask, render_template, request
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
    collection = db.emails
    data = collection.find_one({"emails": []}, {"_id": 0})
    return data
    