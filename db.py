from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
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
    cta_button_color = db.Column(db.String, nullable=False)
    cta_text = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    image_width = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String, nullable=False)
    included_apps = db.relationship("App", secondary=association_table)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "ctaAction": self.cta_action,
            "ctaButtonColor": self.cta_button_color,
            "ctaText": self.cta_text,
            "expirationDate": str(self.expiration_date),
            "includedApps": [app.serialize() for app in self.included_apps],
            "imageHeight": self.image_height,
            "imageUrl": self.image_url,
            "imageWidth": self.image_width,
            "startDate": str(self.start_date),
            "subject": self.subject,
        }


class App(db.Model):
    __tablename__ = "apps"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return self.name
