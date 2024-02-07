from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse
from src.repository import contact as repository_contact
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)) -> Any:
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A negative number is used.")
    elif limit <= skip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The limit is less than or equal to the skip.")
    contact = await repository_contact.get_contacts(skip, limit, current_user, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)) -> Any:
    contact = await repository_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactResponse, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> Any:
    return await repository_contact.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactResponse, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> Any:
    contact = await repository_contact.update_contact(contact_id, current_user, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> Any:
    contact = await repository_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.post("/faker_created_contacts/{contact_id}",
             response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def faker_create_contact(contact_id: int, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)) -> Any:
    return await repository_contact.faker_create_contact(contact_id, current_user, db)


@router.get("/upcoming_birthdays/{days_in_future}", response_model=List[ContactResponse])
async def upcoming_birthdays(days_in_future: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)) -> Any:
    contact = await repository_contact.upcoming_birthdays(days_in_future, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.get("/searchable_by/{choice}", response_model=List[ContactResponse])
async def searchable_by(choice: str, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)) -> Any:
    contact = await repository_contact.searchable_by(choice, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact
