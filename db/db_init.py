from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = "postgresql://bwdublpgniqwgx:663cb1616d830cb812dab169d25fd962145b6ad83006dd09cb5fb0517c07581c" \
                          "@ec2-52-31-70-136.eu-west-1.compute.amazonaws.com:5432/dbhgbaama5ign1"

db = create_engine(SQLALCHEMY_DATABASE_URL)
try:
    db.connect()
except Exception as e:
    print(f"Database conn error: {e}")
print(f"Connection {db.url}")
Base = declarative_base()
