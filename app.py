from db import db
from flask import Flask, request
from functools import wraps
from os import environ
import constants
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


def authenticate(f):
    @wraps(f)
    def inner(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return constants.MISSING_REQUEST_TOKEN_ERROR
        bearer_token = auth_header.replace("Bearer ", "").strip()
        if bearer_token is None or not bearer_token:
            return constants.INVALID_REQUEST_TOKEN_ERROR
        if bearer_token != environ["TOKEN"]:
            return constants.INVALID_REQUEST_TOKEN_ERROR
        return f(*args, **kwargs)

    return inner


@app.route("/create/", methods=["POST"])
@authenticate
def create_announcement():
    post_body = json.loads(request.data)
    res = dao.commit_announcement(post_body)
    return res


@app.route("/update/<id>/", methods=["POST"])
@authenticate
def update(id):
    post_body = json.loads(request.data)
    res = dao.update_announcement(post_body, id)
    return res


@app.route("/delete/<id>/", methods=["DELETE"])
@authenticate
def delete_announcement(id):
    res = dao.delete_announcement(id)
    return res


@app.route("/active/<app>/")
@authenticate
def get_announcements(app):
    res = dao.get_announcements(app)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ["PORT"])
