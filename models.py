from db_init import db, Base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import (Column, ForeignKey, Integer, String, Identity)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1), primary_key=True, unique=True)
    username = Column(String(25), nullable=True, unique=True)
    name = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)
    last_name = Column(String())
    sex = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    token = Column(String(), nullable=False)
    refresh_token = Column(String(), nullable=False)
    organization = relationship("Organization", secondary="org_to_users")

    # def create_user(self, user_data: UserBase):
    #     self.email = user_data.email
    #     self.username = user_data.username
    #     self.name = user_data.name
    #     self.surname = user_data.surname
    #     self.last_name = user_data.last_name
    #     self.sex = user_data.sex


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
SessionLocal = sessionmaker(bind=db, autocommit=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.commit()
        session.close()
# add fixtures
