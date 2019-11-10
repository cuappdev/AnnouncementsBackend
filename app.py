import dao
from db import db
from flask import Flask, request
import json
from os import environ

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
    res = dao.commitAnnouncement(post_body)
    return res


@app.route("/update/<id>/", methods=["POST"])
def update(id):
    post_body = json.loads(request.data)
    res = dao.updateAnnouncement(post_body, id)
    return res


@app.route("/delete/<id>/", methods=["DELETE"])
def delete_announcement(id):
    res = dao.deleteAnnouncement(id)
    return res


@app.route("/active/<app>/")
def get_announcements(app):
    res = dao.getAnnouncements(app)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ["PORT"])
