from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template("main.html")

app.run("0.0.0.0", port=5000)