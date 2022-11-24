from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from db.models import User, get_session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.utils import validate_create_user, user_login

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    auth = user_login(form_data, session)
    headers = {"X-Access-token": auth.get("access_token"), "X-Refresh-token": auth.get('refresh_token')}
    return JSONResponse(content={"message": "Successful login"}, headers=headers)


@router.post("/register")
async def register(form_data: User, session: Session = Depends(get_session)) -> object:
    auth = validate_create_user(form_data, session)
    headers = {"X-Access-token": auth.get("access_token"), "X-Refresh-token": auth.get('refresh_token')}
    return JSONResponse(content={"message": "User is created"}, headers=headers)
# todo: /logout Token = None
# todo: /register


