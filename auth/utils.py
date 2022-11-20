from fastapi import HTTPException
from requests import User
from db.models import User as UserModel, session
from email_validate import validate


def validate_password(user: User, password: str):
    if user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


def validate_create_user(user: User):
    if session.query(UserModel).filter_by(username=user.username).one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    if not validate(email_address=user.email, check_blacklist=False):
        raise HTTPException(status_code=400, detail="Invalid email")
    session.add(UserModel(username=user.username, name=user.name, surname=user.surname,
                         last_name=user.last_name, sex=user.sex, email=user.email, password=user.password))
    session.commit()
    return