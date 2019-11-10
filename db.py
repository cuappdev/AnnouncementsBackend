from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

associationTable = db.Table(
    "association",
    db.Model.metadata,
    db.Column("announcement_id", db.Integer, db.ForeignKey("announcements.id")),
    db.Column("app_id", db.Integer, db.ForeignKey("apps.id")),
)


class Announcement(db.Model):
    __tablename__ = "announcements"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    cta_action = db.Column(db.String, nullable=False)
    cta_text = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String, nullable=False)
    included_apps = db.relationship("App", secondary=associationTable)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "ctaAction": self.cta_action,
            "ctaText": self.cta_text,
            "expirationDate": str(self.expiration_date),
            "includedApps": [app.serialize() for app in self.included_apps],
            "imageUrl": self.image_url,
            "startDate": str(self.start_date),
            "subject": self.subject,
        }


class App(db.Model):
    __tablename__ = "apps"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return self.name
