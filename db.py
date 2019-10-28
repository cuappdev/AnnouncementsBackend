from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Announcement(db.Model):
    __table_name = "announcement"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    ctaText = db.Column(db.String, nullable=False)
    ctaAction = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "imageUrl": self.imageUrl,
            "subject": self.subject,
            "body": self.body,
            "ctaText": self.ctaText,
            "ctaAction": self.ctaAction,
            "expirationDate": str(self.expirationDate),
        }
