from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SQLALCHEMY_DATABASE_URL = "postgresql://ppewkouhaiqytn:069bef344166e587e636165bad350f96d1fcd336e04e51e4e4164d0a7b8e4389" \
                          "@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d86sv7h3k98oga"

db = create_engine(SQLALCHEMY_DATABASE_URL)
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
