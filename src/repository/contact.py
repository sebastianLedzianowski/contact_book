from datetime import datetime, date
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact] | None:
    """
    Get a list of contacts for a specific user.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to retrieve.
        user (User): The user for whom to retrieve contacts.
        db (Session): SQLAlchemy database session.

    Returns:
        List[Contact] | None: List of contacts or None if no contacts are found.
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Get a single contact for a specific user.

    Args:
        contact_id (int): ID of the contact to retrieve.
        user (User): The user for whom to retrieve the contact.
        db (Session): SQLAlchemy database session.

    Returns:
        Contact | None: The contact or None if not found.
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactResponse, user: User, db: Session) -> Contact:
    """
    Create a new contact for a specific user.

    Args:
        body (ContactResponse): Data for the new contact.
        user (User): The user for whom to create the contact.
        db (Session): SQLAlchemy database session.

    Returns:
        Contact: The created contact.
    """
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
    """
    Remove a contact for a specific user.

    Args:
        contact_id (int): ID of the contact to remove.
        user (User): The user for whom to remove the contact.
        db (Session): SQLAlchemy database session.

    Returns:
        Contact | None: The removed contact or None if not found.
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, user: User, body: ContactResponse, db: Session) -> Contact | None:
    """
    Update a contact for a specific user.

    Args:
        contact_id (int): ID of the contact to update.
        user (User): The user for whom to update the contact.
        body (ContactResponse): Data to update the contact.
        db (Session): SQLAlchemy database session.

    Returns:
        Contact | None: The updated contact or None if not found.
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.id = body.id
        contact.name = body.name
        contact.lastname = body.lastname
        contact.birthday = body.birthday
        contact.email = body.email
        contact.phone_number = body.phone_number
        db.commit()
    return contact


async def upcoming_birthdays(days_in_future: int, user: User, db: Session) -> List[Contact] | None:
    """
    Get a list of upcoming birthdays for a specific user.

    Args:
        days_in_future (int): Number of days into the future to consider.
        user (User): The user for whom to retrieve upcoming birthdays.
        db (Session): SQLAlchemy database session.

    Returns:
        List[Contact] | None: List of contacts with upcoming birthdays or None if none found.
    """
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
    """
    Search for contacts based on a specified choice (name, lastname, or email).

    Args:
        choice (str): The choice to search for (name, lastname, or email).
        user (User): The user for whom to perform the search.
        db (Session): SQLAlchemy database session.

    Returns:
        List[Contact] | None: List of contacts matching the search or None if none found.
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    list_contacts = []

    for contact in contacts:
        if choice in [contact.name, contact.lastname, contact.email]:
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
