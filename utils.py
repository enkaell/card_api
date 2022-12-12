from typing import Union
from requests import User
from jose import jwt
from sqlalchemy.orm import Session
from sqlalchemy import or_
from email_validate import validate
from models import User as UserModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
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
    if user := session.query(UserModel).filter(
            or_(UserModel.username == form_data.username, UserModel.username == form_data.username)).one_or_none():
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
    if session.query(UserModel).filter_by(username=user.username).one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    if not validate(email_address=user.email, check_blacklist=False):
        raise HTTPException(status_code=400, detail="Invalid email")

    data = {
        'username': user.username,
        'name': user.name,
        'surname': user.surname,
        'last_name': user.last_name,
        'sex': user.sex, 'email': user.email,
        'password': get_password_hash(user.password),
        'token': create_token(data={'sub': user.username}),
        'refresh_token': create_token(data={'sub': user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES * 7)
    }

    session.add(UserModel(**data))
    return {'access_token': data['token'], 'refresh_token': data['refresh_token'], 'token_type': 'bearer'}


def get_user_profile(token: str, session: Session):
    if user := session.query(UserModel).filter_by(token=token).one_or_none():
        return User(username=user.username, name=user.name, surname=user.surname,
                    last_name=user.name, sex=user.sex, email=user.email, password=user.password)
    raise HTTPException(status_code=404, detail="Not authorized")


def remove_token(token: str, session: Session):
    user = session.query(UserModel).filter_by(token=token).one_or_none()
    user.token = ''
    user.refresh_token = ''
    session.add(user)
    return {'status': 'OK'}

