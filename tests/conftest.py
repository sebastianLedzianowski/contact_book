import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base, User, Contact
from src.database.db import get_db
from src.services.auth import auth_service
from faker import Faker

fake = Faker("pl_PL")

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture(scope="function")
def user():
    class UserTest:
        def __init__(self, id, username, email, password):
            self.id = id
            self.username = username
            self.email = email
            self.password = password

        def dict(self):
            return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "password": self.password
            }
    return UserTest(id=1,
                    username="deadpool",
                    email="deadpool@example.com",
                    password="123456789")


def create_user_db(body: user, db: session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def login_user_confirmed_true_and_hash_password(user, session):
    create_user_db(user, session)
    user_update: User = session.query(User).filter(User.email == user.email).first()
    user_update.password = auth_service.get_password_hash(user_update.password)
    user_update.confirmed = True
    session.commit()


def login_user_token_created(user, session):
    login_user_confirmed_true_and_hash_password(user, session)
    new_user: User = session.query(User).filter(User.email == user.email).first()

    access_token = auth_service.create_access_token(data={"sub": new_user.email})
    refresh_token_ = auth_service.create_refresh_token(data={"sub": new_user.email})

    new_user.refresh_token = refresh_token_
    session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token_, "token_type": "bearer"}


def faker_create_contact(id: int, user: User, db: session) -> dict:
    contact = Contact(
        id=id,
        user_id=user.id,
        name=fake.first_name(),
        lastname=fake.last_name(),
        phone_number=fake.phone_number(),
        email=fake.email(),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=50).strftime('%Y-%m-%d')
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "id": id,
        "user_id": contact.user_id,
        "name": contact.name,
        "lastname": contact.lastname,
        "phone_number": contact.phone_number,
        "email": contact.email,
        "birthday": contact.birthday
    }