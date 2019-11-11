from db import db
from flask import Flask, request
from os import environ
import dao
import json

app = Flask(__name__)

db_filename = environ["DB_FILENAME"]

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/create/", methods=["POST"])
def create_announcement():
    post_body = json.loads(request.data)
    res = dao.commit_announcement(post_body)
    return res


@app.route("/update/<id>/", methods=["POST"])
def update(id):
    post_body = json.loads(request.data)
    res = dao.update_announcement(post_body, id)
    return res


@app.route("/delete/<id>/", methods=["DELETE"])
def delete_announcement(id):
    res = dao.delete_announcement(id)
    return res


@app.route("/active/<app>/")
def get_announcements(app):
    res = dao.get_announcements(app)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ["PORT"])
