from datetime import datetime, date
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactResponse, ContactUpdate

from faker import Faker

fake = Faker("pl_PL")


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    # noinspection PyTypeChecker
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    # noinspection PyTypeChecker
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def created_contact(body: ContactResponse, user: User, db: Session) -> Contact:
    contact = Contact(
        id=body.id,
        user_id=user.id,
        name=body.name,
        lastname=body.lastname,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, user: User, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def faker_created_contact(contact_id: int, user: User, db: Session) -> Contact:
    contact = Contact(
        id=contact_id,
        user_id=user.id,
        name=fake.first_name(),
        lastname=fake.last_name(),
        phone_number=fake.phone_number(),
        email=fake.email(),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=50).strftime('%Y-%m-%d')
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def upcoming_birthdays(days_in_future: int, user: User, db: Session) -> List[Contact] | None:
    today = date.today()
    upcoming_birthdays_list = []
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()

    for contact in contacts:
        birthday = datetime.strptime(contact.birthday, "%Y-%m-%d")
        upcoming_birthday = date(today.year, birthday.month, birthday.day)
        days_to_birthdays = (upcoming_birthday - today).days
        if 0 <= days_to_birthdays <= days_in_future:
            upcoming_birthdays_list.append(Contact(
                id=contact.id,
                user_id=user.id,
                name=contact.name,
                lastname=contact.lastname,
                email=contact.email,
                phone_number=contact.phone_number,
                birthday=contact.birthday
            ))

    return upcoming_birthdays_list


async def searchable_by(choice: str, user: User, db: Session) -> List[Contact] | None:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    list_contacts = []

    for contact in contacts:
        if choice == contact.name or choice == contact.lastname or choice == contact.email:
            list_contacts.append(Contact(
                id=contact.id,
                user_id=user.id,
                name=contact.name,
                lastname=contact.lastname,
                email=contact.email,
                phone_number=contact.phone_number,
                birthday=contact.birthday
            ))
    return list_contacts
