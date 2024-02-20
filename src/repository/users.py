from typing import Type

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

async def get_user_by_email(email: str, db: Session) -> Type[User]:
    """
    Get a user by their email address.

    Args:
        email (str): Email address of the user.
        db (Session): SQLAlchemy database session.

    Returns:
        Type[User]: The user object or None if not found.
    """
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user.

    Args:
        body (UserModel): Data for the new user.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The created user.
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    Args:
        user (User): The user for whom to update the token.
        token (str | None): The new refresh token or None to clear the existing token.
        db (Session): SQLAlchemy database session.
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm the email address for a user.

    Args:
        email (str): Email address to confirm.
        db (Session): SQLAlchemy database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update the avatar for a user.

    Args:
        email (str): Email address of the user.
        url (str): New avatar URL.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The updated user object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
