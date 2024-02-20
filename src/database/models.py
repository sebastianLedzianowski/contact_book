from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.sqltypes import DateTime, Boolean
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class Contact(Base):
    """
     SQLAlchemy model representing a contact.

     Attributes:
         id (int): Primary key for the contact.
         name (str): Name of the contact.
         lastname (str): Last name of the contact.
         email (str): Email address of the contact.
         phone_number (str): Phone number of the contact.
         birthday (str): Birthday of the contact.
         user_id (int): Foreign key referencing the associated user.
         user (relationship): Relationship attribute representing the association with the User model.
     """
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50))
    phone_number = Column(String(30))
    birthday = Column(String(20))
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contact")

class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (int): Primary key for the user.
        username (str): Username of the user.
        email (str): Email address of the user (unique).
        password (str): Password of the user.
        created_at (DateTime): Timestamp indicating when the user was created.
        avatar (str): Filepath to the user's avatar (nullable).
        refresh_token (str): Refresh token for the user (nullable).
        confirmed (bool): Flag indicating whether the user is confirmed.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    def dict(self):
        """
        Convert user data to a dictionary.

        Returns:
            dict: User data as a dictionary.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "refresh_token": self.refresh_token,
            "confirmed": self.confirmed,
        }