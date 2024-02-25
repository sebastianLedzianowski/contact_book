import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.contact import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    upcoming_birthdays,
    searchable_by,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = Contact(
            id=1,
            user_id=self.user.id,
            name="Name",
            lastname="Lastname",
            email="name.lastname@example.com",
            phone_number="123 456 789",
            birthday=(date.today() + timedelta(days=366 * 20)).strftime("%Y-%m-%d")
        )

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)

        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_crate_contact(self):
        body = self.body
        result = await create_contact(body=body, user=self.user, db=self.session)

        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = self.body
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = self.body
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_upcoming_birthdays(self):
        future_birthday = self.body
        self.session.query().filter().all.return_value = [future_birthday]
        result = await upcoming_birthdays(days_in_future=31, user=self.user, db=self.session)

        self.assertEqual(result[0].id, future_birthday.id)
        self.assertEqual(result[0].name, future_birthday.name)
        self.assertEqual(result[0].lastname, future_birthday.lastname)
        self.assertEqual(result[0].email, future_birthday.email)
        self.assertEqual(result[0].phone_number, future_birthday.phone_number)
        self.assertEqual(result[0].birthday, future_birthday.birthday)

    async def test_searchable_by(self):
        search_by = self.body
        self.session.query().filter().all.return_value = [search_by]
        result = await searchable_by(choice="Name", user=self.user, db=self.session)

        self.assertEqual(result[0].id, search_by.id)
        self.assertEqual(result[0].name, search_by.name)
        self.assertEqual(result[0].lastname, search_by.lastname)
        self.assertEqual(result[0].email, search_by.email)
        self.assertEqual(result[0].phone_number, search_by.phone_number)
        self.assertEqual(result[0].birthday, search_by.birthday)