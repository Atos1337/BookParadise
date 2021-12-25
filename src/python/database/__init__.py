from sqlalchemy import create_engine, MetaData
from databases import Database
import os

POSTGRES_URI = os.getenv("DATABASE_URI")
# POSTGRES_URI = "postgresql://postgres:postgres@localhost:8081/postgres"

engine = create_engine(POSTGRES_URI)

meta = MetaData(schema="book_paradise")

db = Database(POSTGRES_URI)


def get_db() -> Database:
    return db
