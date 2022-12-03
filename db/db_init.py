from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
db = create_engine(os.environ['DB_URL'])
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
