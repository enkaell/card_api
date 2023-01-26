from pydantic import Field
from pydantic import BaseModel
from typing import Optional, List


class FrontTag(BaseModel):
    id: int
    name: str


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


class LoginUser(BaseModel):
    username: str
    password: str


class OrgUser(BaseModel):
    id: Optional[int]
    org_id: Optional[int]
    user_id: int


class Organization(BaseModel):
    id: Optional[int]
    name: str


class CreateEvent(BaseModel):
    title: str
    description: Optional[str]
    date: str
    count_people: int
    start_time: str
    address: Optional[str]
    icon_id: Optional[str]
    tags: Optional[List[int]]
    owner: Optional[int]


class UpdateEvent(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    date: Optional[str]
    count_people: Optional[int]
    start_time: Optional[str]
    address: Optional[str]
    icon_id: Optional[str]
    owner: Optional[int]
    tags: Optional[List[int]]


class DeleteEvent(BaseModel):
    id: int


class Event(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: str
    count_people: int
    start_time: str
    address: Optional[str]
    icon_id: Optional[str]
    owner: int
    tags: Optional[List[int]]
    likes: Optional[int]
    dislikes: Optional[int]
    can_join: bool


class FindEvent(BaseModel):
    title: Optional[str]
    description: Optional[str]
    date: Optional[List[str]]
    count_people: Optional[List[int]]
    start_time: Optional[List[str]]
    owner: Optional[List[str]]
    tags: Optional[List[int]]
    sort: Optional[str]


class Set(BaseModel):
    id: int
    name: str
    event_count: int


class JoinEvent(BaseModel):
    id: int


class UserEventTime(BaseModel):
    future_event: List[Event]
    past_event: List[Event]


class AllUserEvent(BaseModel):
    owner: UserEventTime
    member: UserEventTime


class UserWithEvents(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    last_name: str
    sex: str
    email: str
    events: AllUserEvent


class FrontComment(BaseModel):
    event_id: int
    comment: str
