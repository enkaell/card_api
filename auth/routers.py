from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from db.models import get_session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.utils import validate_create_user, user_login, get_user_profile, remove_token
from requests import User as UserRequest

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    auth = user_login(form_data, session)
    auth.update({"message": "Successful login"})
    return JSONResponse(content=auth)


@router.post("/register")
async def register(form_data: UserRequest, session: Session = Depends(get_session)) -> object:
    auth = validate_create_user(form_data, session)
    auth.update({"message": "User is created"})
    return JSONResponse(content=auth)


from main import oauth2_scheme


@router.get("/logout")
async def logout(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return remove_token(token, session)


@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return get_user_profile(token, session)
