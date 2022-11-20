from pydantic import BaseModel
from typing import Optional
from pydantic import Field


class User(BaseModel):
    username: str
    name: str
    surname: str
    last_name: str
    password: str
    sex: str = Field(max_length=6)
    email: str


class OrgUser(BaseModel):
    id: int
    org_id: Optional[int]
    user_id: int


class Organization(BaseModel):
    id: int
    name: str
