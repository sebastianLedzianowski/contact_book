from tests.test_routes_auth import login_user_token_created
from src.routes.users import rate_limit
from PIL import Image
from io import BytesIO


def test_read_users_me(user, session, client):
    token_user = login_user_token_created(user, session)

    response = client.get('/api/users/me/',
                          headers={'Authorization': f'Bearer {token_user.get("access_token")}'},
                          )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == user.username
    assert data["email"] == user.email


def test_update_avatar_user(user, session, client, monkeypatch):
    new_user = login_user_token_created(user, session)

    width, height = 250, 250
    image = Image.new("RGB", (width, height), (255, 0, 0))

    image_bytes_io = BytesIO()
    image.save(image_bytes_io, format="PNG")
    image_bytes_io.seek(0)

    mock_uploaded_file = {"file": ("test_image.png", image_bytes_io, "image/png")}

    response = client.patch(
        "/api/users/avatar",
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"},
        files=mock_uploaded_file
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert "created_at" in data
    assert "avatar" in data
