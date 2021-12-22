from sqlalchemy import Table
from src.python.database import meta, engine

UserRightInDb = Table('userright', meta, autoload=True,
                      autoload_with=engine)
