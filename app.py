from flask import Flask, request
import json
from db import db, Announcement

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
    image_url = post_body.get("image_url")
    subject = post_body.get("subject")
    body = post_body.get("body")
    CTA_text = post_body.get("CTA_text")
    CTA_action = post_body.get("CTA_action")
    announcement = Announcement(
        name=name,
        image_url=image_url,
        subject=subject,
        body=body,
        CTA_text=CTA_text,
        CTA_action=CTA_action,
        is_active=False,
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


@app.route("/activate/", methods=["PUT"])
def activate_announcement():
    post_body = json.loads(request.data)
    name = post_body.get("name")
    announcment = Announcement.query.filter_by(name=name).first()
    if announcment is None:
        return json.dumps({"success": False}), 401
    for ann in Announcement.query.all():
        ann.is_active = False  # Only one announcement is active at a time!
    announcment.is_active = True
    db.session.commit()
    res = {"success": True}
    return json.dumps(res), 200


@app.route("/deactivate/", methods=["PUT"])
def deactivate_announcement():
    post_body = json.loads(request.data)
    name = post_body.get("name")
    announcment = Announcement.query.filter_by(name=name).first()
    if announcment is None:
        return json.dumps({"success": False}), 401
    announcment.is_active = False
    db.session.commit()
    res = {"success": True}
    return json.dumps(res), 200


@app.route("/get_announcement/", methods=["GET"])
def get_announcement():
    active_announcement = Announcement.query.filter_by(is_active=True).first()
    if active_announcement is None:
        return {"data": None}, 200
    res = {"data": active_announcement.serialize()}
    return json.dumps(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
