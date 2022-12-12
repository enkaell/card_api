from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://udwstia2d9myuot38zgl:FhWtzYEVwklXsJtgIdw2@b1qdujwpd8j3ke2gzequ-postgresql.services.clever-cloud.com:5432/b1qdujwpd8j3ke2gzequ'
db = create_engine(SQLALCHEMY_DATABASE_URL)
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
