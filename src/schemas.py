from pydantic import BaseModel, Field, EmailStr

class ContactBase(BaseModel):
    pass


class ContactResponse(ContactBase):
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    birthday: str = Field(max_length=20, example="YYYY-MM-DD")
    id: int
    email: EmailStr | None = Field(default=None)
    phone_number: str = Field(max_length=20, example="+48-876-654-765")

    class Config:
        orm_mode = True

class ContactUpdate(ContactResponse):
    pass