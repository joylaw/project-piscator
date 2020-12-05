import pytest
from app import db
from app.models.User import User
from app.models.EmailAddress import EmailAddress


def test_teardown():
    email = db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    user = db.session.query(User).filter(User.username == 'testuser123').first()

    if email:
        db.session.delete(email)
    if user:
        db.session.delete(user)

    db.session.commit()
