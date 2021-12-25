from sqlalchemy import Table
from database import meta, engine

UserInfoInDb = Table('userinfo', meta, autoload=True,
                     autoload_with=engine)
