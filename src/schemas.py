from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr

class ContactResponse(BaseModel):
    id: int
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    birthday: date
    email: EmailStr | None = Field(default=None)
    phone_number: str = Field(max_length=20, example="+48 876 654 765")

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"