from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException
from db.models import User, session
import uuid
from .utils import validate_password

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if user := session.query(User).filter_by(username=form_data.username).one_or_none():
        validate_password(user, form_data.password)
    else:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    user.token = uuid.uuid4().hex
    session.commit()
    return {"access_token": user.token, "token_type": "bearer"}


@router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()) -> object:
    if not session.query(User).filter_by(username=form_data.username).one_or_none():
        raise HTTPException(status_code=404, detail="Username already taken")
    else:

# todo: /logout Token = None
# todo: /register


