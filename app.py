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
    try:
        past = datetime.strptime(expirationDate, "%m/%d/%Y")
    except:
        return json.dumps({"error": "Please input a valid date of the form 'd/m/y'"})
    announcement = Announcement(
        name=name,
        imageUrl=imageUrl,
        subject=subject,
        body=body,
        ctaText=ctaText,
        ctaAction=ctaAction,
        expirationDate=past,
    )
    db.session.add(announcement)
    db.session.commit()
    res = {"success": True}
    return json.dumps(res), 200


@app.route("/delete/<name>/", methods=["DELETE"])
def delete_announcement(name):
    announcment = Announcement.query.filter_by(name=name).first()
    if announcment is None:
        return json.dumps({"success": False}), 401
    db.session.delete(announcment)
    db.session.commit()
    return json.dumps({"success": True}), 200


@app.route("/get_announcement/", methods=["GET"])
def get_announcement():
    active_announcements = Announcement.query.filter(
        Announcement.expirationDate > datetime.now()
    ).all()
    if active_announcements is None:
        return {"data": None}, 200
    res = {"data": [announcement.serialize() for announcement in active_announcements]}
    return json.dumps(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
