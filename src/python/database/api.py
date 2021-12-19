from sqlalchemy import create_engine, MetaData, Table
from databases import Database

POSTGRES_URI = "postgresql://postgres:postgres@localhost:8081/postgres"

engine = create_engine(POSTGRES_URI)

meta = MetaData(schema="book_paradise")

UserInfoInDb = Table('userinfo', meta, autoload=True,
                     autoload_with=engine)

db = Database(POSTGRES_URI)


def get_db() -> Database:
    return db
