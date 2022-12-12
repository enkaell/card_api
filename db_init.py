from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://tudiejmswmvniv:44741b912599936be0d58e6f87ef2438d9a04bf8c2d5a6de856b36b173e2d8dc@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/d239biaa93na6a'
db = create_engine(SQLALCHEMY_DATABASE_URL)
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
