from db import Announcement, App, db
from datetime import datetime
import constants
import json


def get_app_by_name(name):
    App.query.filter_by(name=name).first()


def valid_date(str):
    return datetime.strptime(str, "%m/%d/%Y")


def assign_apps_to_announcement(announcement, apps):
    announcement.included_apps = []
    for app in apps:
        app_model = get_app_by_name(app)
        if not app_model:
            app_model = App(name=app)
            db.session.add(app_model)
        announcement.included_apps += [app_model]


def commit_announcement(post_body):
    try:
        body = post_body.get("body")
        cta_action = post_body.get("cta_action")
        cta_text = post_body.get("cta_text")
        expiration_date = post_body.get("expiration_date")
        image_url = post_body.get("image_url")
        included_apps = post_body.get("included_apps")
        subject = post_body.get("subject")
        start_date = post_body.get("start_date")
    except:
        return constants.INVALID_REQUEST_BODY_ERROR, 400
    try:
        expiration_date = valid_date(expiration_date)
        start_date = valid_date(start_date)
    except:
        return constants.INVALID_DATE_ERROR, 400
    if not included_apps or not (all(app in constants.VALID_APPS for app in included_apps)):
        return constants.INVALID_APP_NAME_ERROR, 400
    announcement = Announcement(
        body=body,
        cta_action=cta_action,
        cta_text=cta_text,
        expiration_date=expiration_date,
        image_url=image_url,
        start_date=start_date,
        subject=subject,
    )
    assign_apps_to_announcement(announcement, included_apps)
    db.session.add(announcement)
    db.session.commit()
    return constants.SUCCESSFUL_RESPONSE, 201


def update_announcement(post_body, id):
    announcement = Announcement.query.get(id)
    if announcement is None:
        return constants.INVALID_ANNOUNCEMENT_ID_ERROR, 400
    # If any of the keys are not an editable field of Announcement return an error
    if not (all(k in constants.EDITABLE_ANNOUNCEMENT_FIELDS for k in post_body)):
        return constants.INVALID_REQUEST_BODY_ERROR, 400
    for k, v in post_body.items():
        if k == "expiration_date" or k == "start_date":
            try:
                date = valid_date(v)
                setattr(announcement, k, date)
            except:
                return constants.INVALID_DATE_ERROR, 400
        elif k == "included_apps":
            if not v or not (all(app in constants.VALID_APPS for app in v)):
                return constants.INVALID_APP_NAME_ERROR, 400
            else:
                assign_apps_to_announcement(announcement, v)
        else:
            setattr(announcement, k, v)
    db.session.commit()
    return constants.SUCCESSFUL_RESPONSE, 200


def delete_announcement(id):
    announcement = Announcement.query.get(id)
    if not announcement:
        return constants.INVALID_ANNOUNCEMENT_ID_ERROR, 400
    db.session.delete(announcement)
    db.session.commit()
    return constants.SUCCESSFUL_RESPONSE, 200


def get_announcements(app):
    active_announcements = (
        Announcement.query.filter(Announcement.included_apps.any(name=app))
        .filter(Announcement.expiration_date > datetime.now())
        .filter(Announcement.start_date < datetime.now())
        .all()
    )
    res = {
        "success": True,
        "data": [announcement.serialize() for announcement in active_announcements],
    }
    return json.dumps(res), 200
