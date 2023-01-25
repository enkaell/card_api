from jose import jwt
from typing import Union
from sqlalchemy import or_
from core.schemas.schema import User
from fastapi import HTTPException
from sqlalchemy.orm import Session
from email_validate import validate
from passlib.context import CryptContext
from datetime import datetime, timedelta
from core.models.database import UserTable
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_password(user: User, password: str):
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")


def user_login(form_data: OAuth2PasswordRequestForm, session: Session):
    if user := session.query(UserTable).filter(
            or_(UserTable.username == form_data.username, UserTable.username == form_data.username)).one_or_none():
        validate_password(user, form_data.password)
        token = create_token(data={'sub': user.username}),
        refresh_token = create_token(data={'sub': user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES * 7)
        user.refresh_token = refresh_token
        user.token = token
        session.add(user)
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {'access_token': user.token, 'refresh_token': user.refresh_token, 'token_type': 'bearer'}


def validate_create_user(user: User, session: Session):
    if session.query(UserTable).filter(or_(UserTable.username==user.username, UserTable.email==user.email)).one_or_none():
        raise HTTPException(status_code=400, detail="Username or email already taken")
    if not validate(email_address=user.email, check_blacklist=False) or not validate(email_address=user.email, check_blacklist=False):
        raise HTTPException(status_code=400, detail="Invalid email")

    data = user.dict()
    data.update({
        'password': get_password_hash(user.password),
        'token': create_token(data={'sub': user.username}),
        'refresh_token': create_token(data={'sub': user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES * 7) \
    })

    session.add(UserTable(**data))
    return {'access_token': data['token'], 'refresh_token': data['refresh_token'], 'token_type': 'bearer'}


def get_user_profile(token: str, session: Session):
    if user := session.query(UserTable).filter_by(token=token).one_or_none():
        return User(**user.dict())
    raise HTTPException(status_code=404, detail="Not authorized")


def remove_token(token: str, session: Session):
    user = session.query(UserTable).filter_by(token=token).one_or_none()
    user.token = ''
    user.refresh_token = ''
    session.add(user)
    return {'status': 'OK'}


def check_token(func):
    """
    Декоратор для проверки токена
    """
    def _check(*args, **kwargs):
        if user := kwargs.get('session').query(UserTable).filter_by(token=kwargs.get('user')).one_or_none():
            kwargs.update({'user': user.id})
            return func(*args, **kwargs)
        else:
            raise HTTPException(status_code=404, detail="Not authorized")

    return _check
