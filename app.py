from flask import Flask, request
import json
from db import db, Announcement
from datetime import datetime

app = Flask(__name__)

db_filename = "annoucement.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

INVALID_DATE_ERROR = json.dumps(
    {"success": False, "error": "Please input a valid date of the form 'y/m/d'"}
)
INVALID_ANNOUNCEMENT_ERROR = json.dumps(
    {"success": False, "error": "No announcement with that name exists"}
)
INVALID_NAME_ERROR = json.dumps(
    {"success": False, "error": "Announcement with that name already exists"}
)
SUCCESFUL_RESPONSE = json.dumps({"success": True})


@app.route("/create/", methods=["POST"])
def create_announcment():
    post_body = json.loads(request.data)
    name = post_body.get("name")
    imageUrl = post_body.get("imageUrl")
    subject = post_body.get("subject")
    body = post_body.get("body")
    ctaText = post_body.get("ctaText")
    ctaAction = post_body.get("ctaAction")
    expirationDate = post_body.get("expirationDate")
    # Name is an identifier, so there should not be any duplicates.
    if Announcement.query.filter_by(name=name).first() is not None:
        return INVALID_NAME_ERROR, 400
    try:
        expiration = datetime.strptime(expirationDate, "%Y/%m/%d")
    except:
        return INVALID_DATE_ERROR, 400
    announcement = Announcement(
        name=name,
        imageUrl=imageUrl,
        subject=subject,
        body=body,
        ctaText=ctaText,
        ctaAction=ctaAction,
        expirationDate=expiration,
    )
    db.session.add(announcement)
    db.session.commit()
    return SUCCESFUL_RESPONSE, 200


@app.route("/update_expiration_date/", methods=["PUT"])
def update_expiration_date():
    post_body = json.loads(request.data)
    name = post_body.get("name")
    expirationDate = post_body.get("expirationDate")
    try:
        expiration = datetime.strptime(expirationDate, "%Y/%m/%d")
    except:
        return INVALID_DATE_ERROR, 400
    announcement = Announcement.query.filter_by(name=name).first()
    if announcement is None:
        return INVALID_ANNOUNCEMENT_ERROR, 400
    announcement.expirationDate = expiration
    db.session.commit()
    return SUCCESFUL_RESPONSE, 200


@app.route("/delete/<name>/", methods=["DELETE"])
def delete_announcement(name):
    announcment = Announcement.query.filter_by(name=name).first()
    if announcment is None:
        return INVALID_ANNOUNCEMENT_ERROR, 400
    db.session.delete(announcment)
    db.session.commit()
    return SUCCESFUL_RESPONSE, 200


@app.route("/get_announcements/", methods=["GET"])
def get_announcements():
    active_announcements = Announcement.query.filter(
        Announcement.expirationDate > datetime.now()
    ).all()
    if active_announcements == []:
        return json.dumps({"data": None}), 200
    res = {"data": [announcement.serialize() for announcement in active_announcements]}
    return json.dumps(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
