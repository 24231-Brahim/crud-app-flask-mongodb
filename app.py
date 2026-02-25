from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import uuid

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017/")
db = client["gestion_db"]
collection = db["users"]


@app.route("/")
def index():
    users = list(collection.find())
    return render_template("index.html", users=users)


@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        user = {
            "id": str(uuid.uuid4()),
            "name": request.form["name"],
            "email": request.form["email"],
            "age": int(request.form["age"])
        }
        collection.insert_one(user)
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/delete/<id>")
def delete_user(id):
    collection.delete_one({"id": id})
    return redirect(url_for("index"))


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_user(id):
    user = collection.find_one({"id": id})
    if request.method == "POST":
        collection.update_one(
            {"id": id},
            {"$set": {
                "name": request.form["name"],
                "email": request.form["email"],
                "age": int(request.form["age"])
            }}
        )
        return redirect(url_for("index"))
    return render_template("edit_user.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)