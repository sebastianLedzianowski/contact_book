import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.body = User(
            id=1,
            username="Username",
            email="username@example.com",
            password="password",
            created_at="2000-02-02T00:00:00",
            avatar=None,
            refresh_token="refresh_token",
            confirmed=False,
        )

    async def test_get_user_by_email_found(self):
        user = User
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=user.email, db=self.session)

        self.assertEqual(result, user)

    async def test_get_user_by_email_not_fount(self):
        email = "example@example.com"
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=email, db=self.session)

        self.assertIsNone(result)

    async def test_create_user(self):
        body = self.body
        result = await create_user(body=body, db=self.session)

        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.created_at, body.created_at)
        self.assertIsNone(result.avatar)
        self.assertEqual(result.refresh_token, body.refresh_token)
        self.assertFalse(result.confirmed)

    async def test_update_token(self):
        body = self.body
        self.session.query().filter().first.return_value = body
        await update_token(user=body, token="new_token", db=self.session)

        self.assertEqual(body.refresh_token, "new_token")

    async def test_confirmed_email(self):
        body = self.body
        self.session.query().filter().first.return_value = body
        await confirmed_email(email=body.email, db=self.session)

        self.assertTrue(body.confirmed)

    async def test_update_avatar(self):
        body = self.body
        self.session.query().filter().first.return_value = body
        await update_avatar(email=body.email, url="new_avatar", db=self.session)

        self.assertEqual(body.avatar, "new_avatar")
