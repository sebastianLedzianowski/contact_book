from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse, ContactUpdate
from src.repository import contact as repository_contact

router = APIRouter(prefix='/contact', tags=["contact"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.get_contacts(skip, limit, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.post("/", response_model=ContactResponse)
async def created_contact(body: ContactResponse, db: Session = Depends(get_db)) -> Any:
    return await repository_contact.created_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact

@router.post("/faker_created_contacts/{contact_id}", response_model=ContactResponse)
async def faker_created_contact(contact_id: int, db: Session = Depends(get_db)) -> Any:
    return await repository_contact.faker_created_contact(contact_id=contact_id, db=db)


@router.get("/upcoming_birthdays/{days_in_future}", response_model=ContactResponse)
async def upcoming_birthdays(days_in_future: int, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.upcoming_birthdays(days_in_future, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.get("/searchable_by/{choice}", response_model=ContactResponse)
async def searchable_by(choice: str, db: Session = Depends(get_db)) -> Any:
    contact = await repository_contact.searchable_by(choice, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact