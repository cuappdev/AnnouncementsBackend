import Constants
from datetime import datetime
from db import Announcement, App, db
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


def valid_date(str):
    return datetime.strptime(str, "%Y/%m/%d")


@app.route("/create/", methods=["POST"])
def create_announcement():
    post_body = json.loads(request.data)
    try:
        body = post_body.get("body")
        ctaAction = post_body.get("ctaAction")
        ctaText = post_body.get("ctaText")
        expirationDate = post_body.get("expirationDate")
        imageUrl = post_body.get("imageUrl")
        includedApps = post_body.get("includedApps")
        subject = post_body.get("subject")
        startDate = post_body.get("startDate")
    except:
        return Constants.INVALID_REQUEST_BODY_ERROR, 400
    try:
        expiration = valid_date(expirationDate)  # checking for valid date
        start = valid_date(startDate)
    except:
        return Constants.INVALID_DATE_ERROR, 400
    if not (all(app in Constants.VALID_APPS for app in includedApps)) or not includedApps:
        return Constants.INVALID_APP_ERROR, 400
    announcement = Announcement(
        body=body,
        ctaAction=ctaAction,
        ctaText=ctaText,
        expirationDate=expiration,
        imageUrl=imageUrl,
        startDate=start,
        subject=subject,
    )
    for app in includedApps:
        appModel = App.query.filter(App.name == app).first()
        if not appModel:
            appModel = App(name=app)
            db.session.add(appModel)
        announcement.includedApps += [appModel]
    db.session.add(announcement)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 200


@app.route("/update/<id>/", methods=["POST"])
def update(id):
    post_body = json.loads(request.data)
    announcement = Announcement.query.get(id)
    if announcement is None:
        return Constants.INVALID_ANNOUNCEMENT_ERROR, 400
    # If any of the keys are not a field of Announcement return an error
    if not (all(k in (Announcement.__table__.columns + ["includedApps"]) for k in post_body)):
        return Constants.INVALID_REQUEST_BODY_ERROR, 400
    for k, v in post_body.items():
        if k == "expirationDate" or k == "startDate":
            try:
                date = valid_date(v)  # checking for valid date
                setattr(announcement, k, date)
            except:
                return Constants.INVALID_DATE_ERROR, 400
        elif k == "includedApps":
            if not (all(app in Constants.VALID_APPS for app in v)) or not v:
                return Constants.INVALID_APP_ERROR, 400
            else:
                announcement.includedApps = []
                for app in v:
                    appModel = App.query.filter(App.name == app).first()
                    if not appModel:
                        appModel = App(name=app)
                        db.session.add(appModel)
                    announcement.includedApps += [appModel]
        else:
            setattr(announcement, k, v)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 200


@app.route("/delete/<id>/", methods=["DELETE"])
def delete_announcement(id):
    announcement = Announcement.query.get(id)
    if announcement is None:
        return Constants.INVALID_ANNOUNCEMENT_ERROR, 400
    db.session.delete(announcement)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 200


@app.route("/active/<app>/")
def get_announcements(app):
    active_announcements = (
        Announcement.query.filter(Announcement.includedApps.any(name=app))
        .filter(Announcement.expirationDate > datetime.now())
        .filter(Announcement.startDate < datetime.now())
        .all()
    )
    res = {
        "success": True,
        "data": [announcement.serialize() for announcement in active_announcements],
    }
    return json.dumps(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ["PORT"], debug=True)
