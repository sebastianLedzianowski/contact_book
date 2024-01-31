from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    birthday: str = Field(max_length=20, example="YYYY-MM-DD")


class ContactResponse(ContactBase):
    id: int
    email: EmailStr | None = Field(default=None)
    phone_number: PhoneNumber

    class Config:
        orm_mode = True