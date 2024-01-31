from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate, ContactStatusUpdate
from src.repository import contact as repository_contact

router = APIRouter(prefix='/contact', tags=["contact"])


@router.get("/", response_model=List[ContactResponse])
async def read_contact(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    contact = await repository_contact.get_contact(skip, limit, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: id, db: Session = Depends(get_db)):
    contact = await repository_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    return await repository_contact.create_contact(contact_id, body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db())):
    contact = await repository_contact.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_status_contact(body: ContactStatusUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contact.update_status_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contact.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact