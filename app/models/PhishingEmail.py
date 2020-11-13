from app import db
from datetime import datetime

# Defines model for EmailAddress class
class PhishingEmail(db.Model):
    __tablename__ = 'phishing_email'
    mail_id = db.Column(db.Integer, primary_key=True)
    sender_address = db.Column(db.String(30), index=True, unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, index=True,default=datetime.now)

    # FK
    receiver_address = db.Column(db.Integer, db.ForeignKey('email_address.email_id'), index=True, unique=False, nullable=False)

    def __repr__(self):
        return "Phishing Mail from: {} -- Received by: {}".format(self.sender_address, self.receiver_address)