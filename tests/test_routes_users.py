# from src.database.models import User
# from tests.test_routes_auth import login_user_token_created, login_user_confirmed_true_and_hash_password
# from src.routes.users import rate_limit, router


# def test_read_users_me(client, user, session, monkeypatch):
#     access_token = access_token_response(client, user, session, monkeypatch)
#     assert access_token, "Access token is missing or empty"
#
#     response = client.get('/api/users/me/',
#                           headers={'Authorization': f'Bearer {access_token}'},
#                           )
#
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["username"] == user.get('username')
#     assert data["email"] == user.get('email')
#     assert data["password"] == user.get('password')
#
#
# def test_read_users_me_tate_limit(client, user, session, monkeypatch):
#     login_user_token_created(client, session, user, monkeypatch)
#     user_authorization: User = session.query(User).filter(User.email == user.get('email')).first()
#
#     for _ in range(rate_limit.times + 1):
#         response = client.get("/api/users/me/",
#                               headers={'Authorization': f"Bearer {user_authorization.refresh_token}"})
#
#     assert response.status_code == 429, response.text
#     data = response.json()
#     assert data['detail'] == "Too many requests, no more than 10 per minute."
