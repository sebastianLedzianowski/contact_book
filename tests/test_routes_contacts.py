from datetime import timedelta, date

from src.database.models import Contact
from tests.conftest import login_user_token_created, faker_create_contact


def test_read_contacts_a_negative_number_is_used(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.get(
        '/api/contacts/?skip=-1&limit=10',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "A negative number is used."


def test_read_contacts_the_limit_is_less_than_or_equal_to_the_skip(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.get(
        '/api/contacts/?skip=5&limit=3',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "The limit is less than or equal to the skip."


def test_read_contacts(user, session, client):
    new_user = login_user_token_created(user, session)
    new_contact_1 = faker_create_contact(1, user, session)
    new_contact_2 = faker_create_contact(2, user, session)
    new_contact_5 = faker_create_contact(5, user, session)

    response = client.get(
            '/api/contacts/?skip=0&limit=5',
            headers={"Authorization": f"Bearer {new_user.get('access_token')}"})
    assert response.status_code == 200, response.text
    data = response.json()
    for contact in data:
        if contact["id"] == 1:
            assert contact["id"] == new_contact_1.get("id")
            assert contact["name"] == new_contact_1.get("name")
            assert contact["lastname"] == new_contact_1.get("lastname")
            assert contact["birthday"] == new_contact_1.get("birthday")
            assert contact["email"] == new_contact_1.get("email")
            assert contact["phone_number"] == new_contact_1.get("phone_number")
        if contact["id"] == 2:
            assert contact["id"] == new_contact_2.get("id")
            assert contact["name"] == new_contact_2.get("name")
            assert contact["lastname"] == new_contact_2.get("lastname")
            assert contact["birthday"] == new_contact_2.get("birthday")
            assert contact["email"] == new_contact_2.get("email")
            assert contact["phone_number"] == new_contact_2.get("phone_number")
        if contact["id"] == 5:
            assert contact["id"] == new_contact_5.get("id")
            assert contact["name"] == new_contact_5.get("name")
            assert contact["lastname"] == new_contact_5.get("lastname")
            assert contact["birthday"] == new_contact_5.get("birthday")
            assert contact["email"] == new_contact_5.get("email")
            assert contact["phone_number"] == new_contact_5.get("phone_number")

def test_create_contact(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.post(
        '/api/contacts/',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"},
        json={
            "id": 0,
            "name": "example",
            "lastname": "examples",
            "birthday": "2000-02-02",
            "email": "example.examples@example.com",
            "phone_number": "+48 789 987 789"
        }
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["id"] == 0
    assert data["name"] == "example"
    assert data["lastname"] == "examples"
    assert data["birthday"] == "2000-02-02"
    assert data["email"] == "example.examples@example.com"
    assert data["phone_number"] == "+48 789 987 789"


def test_read_contact_is_none(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.get(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found."


def test_read_contact(user, session, client):
    new_user = login_user_token_created(user, session)
    new_contact = faker_create_contact(1, user, session)

    response = client.get(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == new_contact.get("id")
    assert data["name"] == new_contact.get("name")
    assert data["lastname"] == new_contact.get("lastname")
    assert data["birthday"] == new_contact.get("birthday")
    assert data["email"] == new_contact.get("email")
    assert data["phone_number"] == new_contact.get("phone_number")


def test_update_contact_is_none(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.put(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"},
        json={
            "id": 0,
            "name": "example",
            "lastname": "examples",
            "birthday": "2000-02-02",
            "email": "example.examples@example.com",
            "phone_number": "+48 789 987 789"
        }
    )

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found."

def test_update_contact(user, session, client):
    new_user = login_user_token_created(user, session)
    faker_create_contact(1, user, session)

    response = client.put(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"},
        json={
            "id": 0,
            "name": "example",
            "lastname": "examples",
            "birthday": "2000-02-02",
            "email": "example.examples@example.com",
            "phone_number": "+48 789 987 789"
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 0
    assert data["name"] == "example"
    assert data["lastname"] == "examples"
    assert data["birthday"] == "2000-02-02"
    assert data["email"] == "example.examples@example.com"
    assert data["phone_number"] == "+48 789 987 789"


def test_remove_contact_is_none(user, session, client):
    new_user = login_user_token_created(user, session)

    response = client.delete(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found."


def test_remove_contact(user, session, client):
    new_user = login_user_token_created(user, session)
    new_contact = faker_create_contact(1, user, session)

    response = client.delete(
        'api/contacts/1',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 200, response.txt
    data = response.json()
    assert data["id"] == new_contact.get("id")
    assert data["name"] == new_contact.get("name")
    assert data["lastname"] == new_contact.get("lastname")
    assert data["birthday"] == new_contact.get("birthday")
    assert data["email"] == new_contact.get("email")
    assert data["phone_number"] == new_contact.get("phone_number")


def test_upcoming_birthday_no_contact(user, session, client):
    new_user = login_user_token_created(user, session)
    birthday = date.today() + timedelta(days=10)
    contact = Contact(
            id=0,
            user_id=user.id,
            name="example",
            lastname="examples",
            birthday=birthday,
            email="example.examples@example.com",
            phone_number="+48 789 987 789"
    )
    session.add(contact)
    session.commit()
    session.refresh(contact)

    response = client.get(
        '/api/contacts/upcoming_birthdays/7',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_upcoming_birthday(user, session, client):
    new_user = login_user_token_created(user, session)

    contact_1 = Contact(
            id=1,
            user_id=user.id,
            name="Jakub",
            lastname="Nowak",
            birthday=date.today() + timedelta(days=3),
            email="jakub.nowak@example.com",
            phone_number="+48 111 111 111"
    )
    session.add(contact_1)
    session.commit()
    session.refresh(contact_1)

    contact_2 = Contact(
        id=2,
        user_id=user.id,
        name="Adam",
        lastname="Kowalski",
        birthday=date.today() + timedelta(days=10),
        email="adam.kowalski@example.com",
        phone_number="+48 222 222 222"
    )
    session.add(contact_2)
    session.commit()
    session.refresh(contact_2)

    response = client.get(
        '/api/contacts/upcoming_birthdays/7',
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 200, response.text
    data = response.json()
    for contact in data:
        assert contact["id"] == contact_1.id
        assert contact["name"] == contact_1.name
        assert contact["lastname"] == contact_1.lastname
        assert contact["birthday"] == contact_1.birthday
        assert contact["email"] == contact_1.email
        assert contact["phone_number"] == contact_1.phone_number


def test_searchable_by(user, session, client):
    new_user = login_user_token_created(user, session)

    contact_1 = Contact(
            id=1,
            user_id=user.id,
            name="Jakub",
            lastname="Nowak",
            birthday=date.today() + timedelta(days=3),
            email="jakub.nowak@example.com",
            phone_number="+48 111 111 111"
    )
    session.add(contact_1)
    session.commit()
    session.refresh(contact_1)

    contact_2 = Contact(
        id=2,
        user_id=user.id,
        name="Adam",
        lastname="Kowalski",
        birthday=date.today() + timedelta(days=10),
        email="adam.kowalski@example.com",
        phone_number="+48 222 222 222"
    )
    session.add(contact_2)
    session.commit()
    session.refresh(contact_2)

    response = client.get(
        "/api/contacts/searchable_by/Adam",
        headers={"Authorization": f"Bearer {new_user.get('access_token')}"})

    assert response.status_code == 200, response.text
    data = response.json()
    for contact in data:
        assert contact["id"] == contact_2.id
        assert contact["name"] == contact_2.name
        assert contact["lastname"] == contact_2.lastname
        assert contact["birthday"] == contact_2.birthday
        assert contact["email"] == contact_2.email
        assert contact["phone_number"] == contact_2.phone_number