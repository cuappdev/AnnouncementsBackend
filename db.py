from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Announcement(db.Model):
    __table_name = "announcement"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    CTA_text = db.Column(db.String, nullable=False)
    CTA_action = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "imageUrl": self.image_url,
            "subject": self.subject,
            "body": self.body,
            "ctaText": self.CTA_text,
            "ctaAction": self.CTA_action,
            "is_active": self.is_active,
        }
