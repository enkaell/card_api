from db.models import User
from fastapi import HTTPException


def validate_password(user: User, password: str):
    if user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

