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
    ctaAction = db.Column(db.String, nullable=False)
    ctaText = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String, nullable=False)
    includedApps = db.relationship("App", secondary=associationTable)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "ctaAction": self.ctaAction,
            "ctaText": self.ctaText,
            "expirationDate": str(self.expirationDate),
            "includedApps": [app.serialize() for app in self.includedApps],
            "imageUrl": self.imageUrl,
            "startDate": str(self.startDate),
            "subject": self.subject,
        }


class App(db.Model):
    __tablename__ = "apps"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return self.name
