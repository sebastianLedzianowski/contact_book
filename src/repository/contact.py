from typing import List
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactResponse, ContactUpdate

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
