import Constants
from db import Announcement, App, db
from datetime import datetime
import json


def getAppByName(name):
    App.query.filter(App.name == name).first()


def valid_date(str):
    return datetime.strptime(str, "%Y/%m/%d")


def assignAppsToAnnouncement(announcement, apps):
    announcement.includedApps = []
    for app in apps:
        appModel = getAppByName(app)
        if not appModel:
            appModel = App(name=app)
            db.session.add(appModel)
        announcement.includedApps += [appModel]


def commitAnnouncement(post_body):
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
    assignAppsToAnnouncement(announcement, includedApps)
    db.session.add(announcement)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 201


def updateAnnouncement(post_body, id):
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
                assignAppsToAnnouncement(announcement, v)
        else:
            setattr(announcement, k, v)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 200


def deleteAnnouncement(id):
    announcement = Announcement.query.get(id)
    if announcement is None:
        return Constants.INVALID_ANNOUNCEMENT_ERROR, 400
    db.session.delete(announcement)
    db.session.commit()
    return Constants.SUCCESSFUL_RESPONSE, 200


def getAnnouncements(app):
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
