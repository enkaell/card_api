from db.db_init import db, Base
from sqlalchemy import (Column, ForeignKey, Integer, String, Date, Identity, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1), primary_key=True, unique=True)
    username = Column(String(25), primary_key=True)
    name = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)
    last_name = Column(String())
    dateborn = Column(Date(), nullable=False)
    sex = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    token = Column(
        UUID(as_uuid=False),
        server_default=text("gen_random_uuid()"),
        unique=True,
        nullable=True,
        index=True,
    )
    organization = relationship("Organization", secondary="org_to_users")


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, Identity(start=1), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner = relationship("User", secondary="org_to_users")


class OrgUser(Base):
    __tablename__ = "org_to_users"
    id = Column(Integer, Identity(start=1), primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(db)
session = Session(db)
# add fixtures
