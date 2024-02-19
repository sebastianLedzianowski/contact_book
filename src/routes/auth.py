from fastapi import APIRouter, Depends, status, Security, BackgroundTasks, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.services.email import send_email
from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)

    if exist_user:
        return JSONResponse(status_code=409, content={"detail": "Account already exists."})

    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)

    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}



@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)

    if user is None:
        return JSONResponse(status_code=401, content={"detail": "Invalid email."})

    if not user.confirmed:
        return JSONResponse(status_code=401, content={"detail": "Email not confirmed."})

    if not auth_service.verify_password(body.password, user.password):
        return JSONResponse(status_code=401, content={"detail": "Invalid password."})

    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token_ = await auth_service.create_refresh_token(data={"sub": user.email})

    await repository_users.update_token(user, refresh_token_, db)
    return {"access_token": access_token, "refresh_token": refresh_token_, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)

    user = await repository_users.get_user_by_email(email, db)

    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        return JSONResponse(status_code=401, content={"detail": "Invalid refresh token."})

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token_ = await auth_service.create_refresh_token(data={"sub": email})

    await repository_users.update_token(user, refresh_token_, db)
    return {"access_token": access_token, "refresh_token": refresh_token_, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        return JSONResponse(status_code=400, content={"detail": "Verification error."})
    if user.confirmed:
        return {"message": "Your email is already confirmed."}

    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed."}

@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed."}
    if user.confirmed is False:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
        return {"message": "Check your email for confirmation."}