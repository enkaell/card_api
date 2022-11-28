from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@api-db1:5432/api"
db = create_engine(SQLALCHEMY_DATABASE_URL)
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
