from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactResponse, ContactUpdate

from faker import Faker

fake = Faker("pl_PL")


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    # noinspection PyTypeChecker
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    # noinspection PyTypeChecker
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def created_contact(body: ContactResponse, db: Session) -> Contact:
    contact = Contact(
        id=body.id,
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


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def upcoming_birthdays(days_in_future: int, db: Session) -> List[Dict[str, Any]] | None:
    contacts = db.query(Contact).all()
    today = date.today()
    today_to_birthday = today + timedelta(days=days_in_future)
    coming_birthdays = []

    for contact in contacts:
        birthday = datetime.strptime(contact.birthday, "%Y-%m-%d")
        upcoming_birthday = date(today.year, birthday.month, birthday.day)
        days_to_birthdays = (upcoming_birthday - today).days

        if today.day == birthday.day and today.month == birthday.month:
            coming_birthdays.append({"name": contact.name,
                                     "lastname": contact.lastname,
                                     "phone_number": contact.phone_number,
                                     "days_to_birthday": days_to_birthdays
                                     })

        if today < upcoming_birthday <= today_to_birthday:
            coming_birthdays.append({"name": contact.name,
                                     "lastname": contact.lastname,
                                     "phone_number": contact.phone_number,
                                     "days_to_birthday": days_to_birthdays
                                     })
    return coming_birthdays


async def faker_created_contact(contact_id: int, db: Session) -> Contact:
    contact = Contact(
        id=contact_id,
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
