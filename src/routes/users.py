from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])

rate_limit = RateLimiter(times=10, seconds=60)

@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)) -> UserDb:
    """
    Read the authenticated user's profile.

    Args:
        current_user (User): The authenticated user.

    Returns:
        UserDb: The user's profile.
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(),
                             current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)) -> UserDb:
    """
    Update the avatar for the authenticated user.

    Args:
        file (UploadFile): Uploaded file containing the new avatar image.
        current_user (User): The authenticated user.
        db (Session): SQLAlchemy database session.

    Returns:
        UserDb: The updated user profile.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'contact_book/{current_user.email}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'contact_book/{current_user.email}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
