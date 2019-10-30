from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Announcement(db.Model):
    __table_name = "announcement"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    ctaAction = db.Column(db.String, nullable=False)
    ctaText = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "ctaAction": self.ctaAction,
            "ctaText": self.ctaText,
            "expirationDate": str(self.expirationDate),
            "imageUrl": self.imageUrl,
            "subject": self.subject,
        }
