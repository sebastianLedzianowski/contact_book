import json
from unittest.mock import MagicMock

from src.database.models import User


def create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    return response


def login_user_confirmed_true(client, session, user, monkeypatch):
    create_user(client, user, monkeypatch)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()


def login_user_token_created(client, session, user, monkeypatch):
    login_user_confirmed_true(client, session, user, monkeypatch)
    client.post("/api/auth/login", data={"username": user.get('email'), "password": user.get('password')})


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists."


def test_login_wrong_email(client, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.post(
        "/api/auth/login",
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email."


def test_login_user_not_confirmed(client, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed."


def test_login_wrong_password(client, session, user, monkeypatch):
    create_user(client, user, monkeypatch)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password."


def test_login_user(client, session, user, monkeypatch):
    login_user_confirmed_true(client, session, user, monkeypatch)
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_request_email(client, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.post(
        "/api/auth/request_email",
        data=json.dumps({"email": user.get('email')}),
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Check your email for confirmation."


def test_request_email_confirmed(client, session, user, monkeypatch):
    login_user_confirmed_true(client, session, user, monkeypatch)
    response = client.post(
        "/api/auth/request_email",
        data=json.dumps({"email": user.get('email')}),
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Your email is already confirmed."


def test_refresh_token_user_not_found(client, session, user, monkeypatch):
    login_user_token_created(client, session, user, monkeypatch)
    user = session.query(User).filter(User.email == user.get('email')).first()
    response = client.get(
        '/api/auth/refresh_token',
        headers={
            'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsZWR6aWFub3dza2lAbzIucGwiLCJpYXQiOjE3MDc4NDY5NDMsImV4cCI6MTcwODQ1MTc0Mywic2NvcGUiOiJyZWZyZXNoX3Rva2VuIn0.VLX28ls8AB6-JHWkKynSRFktDDk-Gteb0vMbS9dDppE'}
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'User not found.'


def test_refresh_token(client, session, user, monkeypatch):
    login_user_token_created(client, session, user, monkeypatch)
    user_authorization: User = session.query(User).filter(User.email == user.get('email')).first()
    response = client.get(
        '/api/auth/refresh_token',
        headers={'Authorization': f"Bearer {user_authorization.refresh_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'token_type' in data


def test_confirmed_email_user_is_none(client, session, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.get(
        '/api/auth/confirmed_email/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbmNsdWRpbmdAbzIucGwiLCJpYXQiOjE3MDc5MzQwNTQsImV4cCI6MTcwODUzODg1NH0.UCeSStDqYvSXGjiR7WHaLPstjh9yQZHC6s9kAm00NmI'
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Verification error.'


def test_confirmed_email_user_confirmed(client, session, user, monkeypatch):
    login_user_confirmed_true(client, session, user, monkeypatch)
    response = client.get(
        'http://localhost:8000/api/auth/confirmed_email/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbmNsdWRpbmdAbzIucGwiLCJpYXQiOjE3MDc5MzQwNTQsImV4cCI6MTcwODUzODg1NH0.UCeSStDqYvSXGjiR7WHaLPstjh9yQZHC6s9kAm00NmI'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Your email is already confirmed.'


def test_confirmed_email(client, user, monkeypatch):
    create_user(client, user, monkeypatch)
    response = client.get(
        'http://localhost:8000/api/auth/confirmed_email/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbmNsdWRpbmdAbzIucGwiLCJpYXQiOjE3MDc5MzQwNTQsImV4cCI6MTcwODUzODg1NH0.UCeSStDqYvSXGjiR7WHaLPstjh9yQZHC6s9kAm00NmI'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Email confirmed.'