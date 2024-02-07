from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from services.auth import auth_service

import environ

env = environ.Env(DEBUG=(bool, True), EMAIL_USE_TLS=(bool, True), EMAIL_USE_SSL=(bool, True))
environ.Env.read_env()

conf = ConnectionConfig(
    MAIL_USERNAME=env("MAIL_USERNAME"),
    MAIL_PASSWORD=env("MAIL_PASSWORD"),
    MAIL_FROM=EmailStr("example@example.com"),
    MAIL_PORT=env("MAIL_PORT"),
    MAIL_SERVER=env("MAIL_SERVER"),
    MAIL_FROM_NAME=env("MAIL_FROM_NAME"),
    MAIL_STARTTLS=env("MAIL_STARTTLS"),
    MAIL_SSL_TLS=env("MAIL_SSL_TLS"),
    USE_CREDENTIALS=env("USE_CREDENTIALS"),
    VALIDATE_CERTS=env("VALIDATE_CERTS"),
    TEMPLATE_FOLDER=env("TEMPLATE_FOLDER"),
)

async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
