from pydantic import BaseModel
from typing import Optional
from pydantic import Field


class CreateUser(BaseModel):
    username: str
    name: str
    surname: str
    last_name: str
    password: str
    sex: str = Field(max_length=6)
    email: str


class User(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    last_name: str
    password: str
    sex: str = Field(max_length=6)
    email: str


class OrgUser(BaseModel):
    id: Optional[int]
    org_id: Optional[int]
    user_id: int


class Organization(BaseModel):
    id: Optional[int]
    name: str


class CreateEvent(BaseModel):
    title: str
    date: str
    count_people: int
    start_time: str
    address: Optional[str]
    icon_id: Optional[str]
    tags: Optional[list]
    owner: Optional[int]


class UpdateEvent(BaseModel):
    id: int
    title: Optional[str]
    date: Optional[str]
    count_people: Optional[int]
    start_time: Optional[str]
    address: Optional[str]
    icon_id: Optional[str]
    owner: Optional[int]
    tags: Optional[list]


class DeleteEvent(BaseModel):
    id: int


class Event(BaseModel):
    id: int
    title: str
    date: str
    count_people: int
    start_time: str
    address: Optional[str]
    icon_id: Optional[str]
    owner: int
    tags: Optional[list]