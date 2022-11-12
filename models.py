from main import db, Base
from sqlalchemy import (Column, ForeignKey, Integer, String, Date)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False)
    name = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)
    last_name = Column(String())
    dateborn = Column(Date(), nullable=False)
    sex = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    token = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization = relationship("Organization", secondary="org_to_users")


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner = relationship("User", secondary="org_to_users")


class OrgUser(Base):
    __tablename__ = "org_to_users"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(db)

with Session(bind=db) as session:
    u1 = User(id=1, username="vlad2012", name="Vlad", surname="Chesnokov",
              dateborn="11.11.2011", sex="M", email="vlad@mail.ru")
    session.add(u1)
    o1 = Organization(name="Gay Club")
    session.add(o1)
    o1.owner = [u1]
    session.commit()
