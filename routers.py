from typing import List
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from core.models.database import get_session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from core.auth.service import validate_create_user, user_login, get_user_profile, remove_token
from core.schemas.schema import User, CreateUser, LoginUser, Event, CreateEvent, UpdateEvent, DeleteEvent, FrontTag, \
    Set, FindEvent
from core.events.service import add_event, read_events, read_my_events, change_event, delete_event, map_tags, read_sets, \
    like_dislike_event, join_event


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.post("/login", tags=['account'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    auth = user_login(LoginUser(username=form_data.username, password=form_data.password), session)
    auth.update({"message": "Successful login"})
    profile = get_user_profile(auth.get('access_token'), session)
    auth.update(**profile.dict())
    return JSONResponse(content=auth)


@router.post("/register", tags=['account'])
async def register(form_data: CreateUser, session: Session = Depends(get_session)) -> object:
    auth = validate_create_user(form_data, session)
    auth.update({"message": "User is created"})
    return JSONResponse(content=auth)


@router.get("/logout", tags=['account'])
async def logout(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return remove_token(token, session)


@router.get("/profile", response_model=User, tags=['account'])
async def get_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return get_user_profile(token, session)


# @router.get('/user_profile', response_model=)


@router.post('/events/create', tags=['events'])
async def create_event(event: CreateEvent, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return add_event(user=token, session=session, event=event)


@router.post('/events/update', tags=['events'])
async def update_event(event: UpdateEvent, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return change_event(user=token, session=session, event=event)


@router.post('/events/delete', tags=['events'])
async def remove_event(event: DeleteEvent, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return delete_event(user=token, session=session, event=event)


@router.get('/events', response_model=List[Event], tags=['events'])
async def get_events(session: Session = Depends(get_session), id: int = None):
    return read_events(session, id=id)


@router.get('/events/my', response_model=List[Event], tags=['events'])
async def get_my_events(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return read_my_events(user=token, session=session)


@router.post('/find', response_model=List[Event], tags=['events'])
async def find_events(filter: FindEvent, session: Session = Depends(get_session)):
    return read_events(session, **filter.dict())


@router.get('/tags', response_model=List[FrontTag], tags=['events'])
async def get_tags():
    return [FrontTag(id=value, name=key) for key, value in map_tags.items()]


@router.get('/sets', response_model=List[Set], tags=['events'])
async def get_sets(session: Session = Depends(get_session)):
    return read_sets(session)


@router.post('/like', tags=['events'])
async def like_event(id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return like_dislike_event(user=token, id=id, action='likes', session=session)


@router.post('/dislike', tags=['events'])
async def dislike_event(id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return like_dislike_event(user=token, id=id, action='dislikes', session=session)


@router.post('/join', tags=['events'])
async def join(id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return join_event(user=token, id=id, session=session)


app.include_router(router)
