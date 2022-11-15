from pydantic import BaseModel
from typing import Optional
import datetime


class User(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    last_name: str
    date: datetime.date
    sex: str
    email: str
    token: str


class OrgUser(BaseModel):
    id: int
    org_id: Optional[int]
    user_id: int


class Organization(BaseModel):
    id: int
    name: str
