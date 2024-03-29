from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr

class ContactResponse(BaseModel):
    """
    Schema for the response of a contact.
    """
    id: int
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    birthday: date
    email: EmailStr | None = Field(default=None)
    phone_number: str = Field(max_length=20, example="+48 876 654 765")

    class ConfigDict:
        from_attributes = True


class UserModel(BaseModel):
    """
    Schema for user input during registration.
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Schema for user data retrieved from the database.
    """
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str | None

    class ConfigDict:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Schema for the response after user creation.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Schema for the response containing access and refresh tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    """
    Schema for the request containing an email address.
    """
    email: EmailStr
