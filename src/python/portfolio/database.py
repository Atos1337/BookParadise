from sqlalchemy import Table
from database import meta, engine

PortfolioBookInDb = Table('portfoliobook', meta, autoload=True,
                          autoload_with=engine)

PortfolioRecordInDb = Table('portfoliorecord', meta, autoload=True,
                            autoload_with=engine)
