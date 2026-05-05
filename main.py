from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

from pymongo.mongo_client import MongoClient

client = MongoClient(os.getenv("uri"))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("uri")
mongo = PyMongo(app)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/Submit", methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    gender = request.form.get("gender")
    
    document = {
        "Name": name,
        "Email": email,
        "Gender": gender
    }

    try:
        mongo.db.yummy.insert_one(document)
        return redirect(url_for("success"))   # fixed naming
    except Exception as e:
        return f"Another Failure : {str(e)}"


@app.route("/success")
def success():   # fixed function name
    return "Data submitted successfully"


# 🔥 NEW /api ROUTE (Task 2)
@app.route("/api")
def api():
    return jsonify({
        "name": "Rishabh Jain",
        "project": "Flask MongoDB",
        "status": "updated in JainRishab_new branch",
        "task": "Task 2 completed"
    })


if __name__ == "__main__":
    app.run(debug=True)