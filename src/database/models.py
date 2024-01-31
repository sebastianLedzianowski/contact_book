from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = EmailStr
    phone_number = PhoneNumber
    birthday = Column(String(20))
    done = Column(Boolean, default=False)