# from pydantic import BaseModel
# from typing import Optional
# import datetime
# import uuid
#
#
# class User(BaseModel):
#     id: int
#     username: str
#     name: str
#     surname: str
#     last_name: str
#     date: datetime.date
#     sex: str
#     email: str
#     organization: Optional[int]
#     token: uuid.uuid4
#
#
# class OrgUser(BaseModel):
#     id: int
#     org_id: Optional[int]
#     user_id: User.id
#
# # class Organization(BaseModel):
