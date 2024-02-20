from tests.test_routes_auth import login_user_token_created
from src.routes.users import rate_limit


def test_read_users_me(user, session, client):
    token_user = login_user_token_created(user, session)

    response = client.get('/api/users/me/',
                          headers={'Authorization': f'Bearer {token_user.get("access_token")}'},
                          )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == user.username
    assert data["email"] == user.email


def test_read_users_me_tate_limit(user, session, client):
    token_user = login_user_token_created(user, session)

    for _ in range(rate_limit.times + 1):
        response = client.get("/api/users/me/",
                              headers={'Authorization': f'Bearer {token_user.get("access_token")}'})

    assert response.status_code == 429, response.text
    data = response.json()
    assert data['detail'] == "Too many requests, no more than 10 per minute."
