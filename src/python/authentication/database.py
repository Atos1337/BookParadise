from sqlalchemy import Table
from src.python.database import meta, engine

UserInfoInDb = Table('userinfo', meta, autoload=True,
                     autoload_with=engine)
