import json
from unittest.mock import MagicMock, AsyncMock
from src.database.models import User
from src.repository.users import update_token, get_user_by_email
from src.services.auth import auth_service
from tests.conftest import session, user


def create_user_db(body: user, db: session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def login_user_confirmed_true_and_hash_password(user, session):
    create_user_db(user, session)
    user_update: User = session.query(User).filter(User.email == user.email).first()
    user_update.password = auth_service.get_password_hash(user_update.password)
    user_update.confirmed = True
    session.commit()


async def login_user_token_created(user, session):
    login_user_confirmed_true_and_hash_password(user, session)
    session.commit()
    new_user: User = session.query(User).filter(User.email == user.email).first()

    access_token = auth_service.create_access_token(data={"sub": new_user.email})
    refresh_token_ = auth_service.create_refresh_token(data={"sub": new_user.email})

    return {"access_token": access_token, "refresh_token": refresh_token_, "token_type": "bearer"}

async def user_refresh_token_saved(user, session):
    response = await login_user_token_created(user, session)
    data = response.__dict__
    new_user: User = session.query(User).filter(User.email == user.email).first()
    new_user.refresh_token = data.get('refresh_token')
    session.commit()

def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)

    response = client.post("/api/auth/signup", json=user.dict())

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.email
    assert "id" in data["user"]


def test_repeat_create_user(user, session, client):
    create_user_db(user, session)

    response = client.post("/api/auth/signup", json=user.dict())

    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists."


def test_login_wrong_email(user, session, client):
    create_user_db(user, session)

    response = client.post(
        "/api/auth/login",
        data={"username": 'email', "password": user.password},
    )

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email."


def test_login_user_not_confirmed(user, session, client):
    create_user_db(user, session)

    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": user.password},
    )

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed."


def test_login_wrong_password(user, session, client):
    login_user_confirmed_true_and_hash_password(user, session)

    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": 'password'},
    )

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password."


def test_login_user(user, session, client):
    login_user_confirmed_true_and_hash_password(user, session)

    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": user.password},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid_user(user, session, client, monkeypatch):
    login_user_token_created(user, session)

    async def mock_decode_refresh_token(token):
        return user.email

    monkeypatch.setattr(auth_service, "decode_refresh_token", AsyncMock(side_effect=mock_decode_refresh_token))

    response = client.get(
        '/api/auth/refresh_token',
        headers={
            'Authorization': f'Bearer invalid_refresh_token'}
    )

    assert response.status_code == 401
    data = response.json()
    assert data['detail'] == 'Invalid refresh token.'


def test_refresh_token(user, session, client):
    login_user_token_created(user, session)
    user_authorization: User = session.query(User).filter(User.email == user.email).first()

    response = client.get(
        '/api/auth/refresh_token',
        headers={'Authorization': f"Bearer {user_authorization.refresh_token}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data["token_type"] == "bearer"


def test_confirmed_email_user_is_none(user, session, client):
    create_user_db(user, session)
    response = client.get(
        '/api/auth/confirmed_email/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbmNsdWRpbmdAbzIucGwiLCJpYXQiOjE3MDc5MzQwNTQsImV4cCI6MTcwODUzODg1NH0.UCeSStDqYvSXGjiR7WHaLPstjh9yQZHC6s9kAm00NmI'
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Verification error.'


def test_confirmed_email_user_confirmed(user, session, client, monkeypatch):
    login_user_confirmed_true_and_hash_password(user, session)

    async def mock_decode_confirmed_email_token(token):
        return user.email

    monkeypatch.setattr(auth_service, "get_email_from_token",
                        AsyncMock(side_effect=mock_decode_confirmed_email_token))

    response = client.get(
        f'/api/auth/confirmed_email/your_email_is_already_confirmed'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Your email is already confirmed.'


def test_confirmed_email(user, session, client, monkeypatch):
    create_user_db(user, session)

    async def mock_decode_confirmed_email_token(token):
        return user.email

    monkeypatch.setattr(auth_service, "get_email_from_token",
                        AsyncMock(side_effect=mock_decode_confirmed_email_token))

    response = client.get(
        '/api/auth/confirmed_email/email_confirmed'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Email confirmed.'


def test_request_email_confirmed(user, session, client, monkeypatch):
    login_user_confirmed_true_and_hash_password(user, session)

    response = client.post(
        "/api/auth/request_email",
        data=json.dumps({"email": user.email}),
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Your email is already confirmed."


def test_request_email(user, session, client):
    create_user_db(user, session)

    response = client.post(
        "/api/auth/request_email",
        data=json.dumps({"email": user.email}),
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Check your email for confirmation."