from sqlalchemy import Table
from database import meta, engine

UserRightInDb = Table('userright', meta, autoload=True,
                      autoload_with=engine)
