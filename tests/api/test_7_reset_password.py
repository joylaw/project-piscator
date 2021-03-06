import pytest
from test_2_authentication import login, logout
from test_3_add_email import add_mail
from app.models.User import User
from app import db
from app.utils.DBUtils import get_user_by_name
from app.utils.FileUtils import get_server_mail_cred
from app.utils.DBUtils import get_email_address_by_address

def request_reset_password(client, db, username, email_address):
    return client.post(
    '/reset', data={
    'username' : username,
    'email_address' : email_address
    },
    follow_redirects=True
    )

def update_new_password(client, db, new_password, token):
    return client.post(
    '/reset/change_password', data={
        'token_received' : token,
        'new_password' : new_password
    },
    follow_redirects=True
    )

# Test valid reset password request
def test_request_reset_password(client, db):
    # Creates a new user
    TEST_RESET_USER = 'resetmyaccount'
    TEST_RESET_PASSWORD = 'password'

    new_user = User(username=TEST_RESET_USER)
    new_user.set_password(TEST_RESET_PASSWORD)
    db.session.add(new_user)
    db.session.commit()

    # Logs in to user and add an email address and log out
    login_response = login(client, TEST_RESET_USER, TEST_RESET_PASSWORD)
    assert login_response.status_code == 200
    assert b'dashboard' in login_response.data

    MAIL_CREDS = get_server_mail_cred()
    TEST_EMAIL_ADDRESS = MAIL_CREDS[2]
    TEST_EMAIL_PASSWORD = MAIL_CREDS[3]
    response = add_mail(client, TEST_EMAIL_ADDRESS, TEST_EMAIL_PASSWORD)
    assert response.status_code == 200
    assert get_email_address_by_address(TEST_EMAIL_ADDRESS)
    assert b'piscator.honeypot@outlook.com' in response.data

    logout(client)

    reset_response = request_reset_password(client, db, TEST_RESET_USER\
    , TEST_EMAIL_ADDRESS)
    # Assert redirected to update password page
    assert b'token' in reset_response.data
    # Assert token is generated
    assert get_user_by_name(TEST_RESET_USER).get_reset_token()

# Test valid reset password update
def test_update_forgotten_password(client, db):
    TEST_RESET_USER = 'resetmyaccount'
    NEW_PASSWORD = 'pa$$w0rd'
    USER_ENTITY = get_user_by_name(TEST_RESET_USER)
    TOKEN_VALUE = USER_ENTITY.get_reset_token()

    # Creates a session variable for id to be passed in to route
    with client.session_transaction() as sess:
        sess['reset_user_id'] = USER_ENTITY.get_id()

    # Sends a post request to change_password with retrieved token
    r = client.post(
    '/reset/change_password', data={
    'token' : TOKEN_VALUE,
    'new_password' : NEW_PASSWORD
    },
    follow_redirects=True
    )

    login_response = login(client, TEST_RESET_USER, NEW_PASSWORD)

    # Assert TEST_RESET_USER token is None
    assert not get_user_by_name(TEST_RESET_USER).get_reset_token()
    # Assert successful login with new password
    assert login_response.status_code == 200
    assert b'dashboard' in login_response.data
