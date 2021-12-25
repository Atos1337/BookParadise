from sqlalchemy import Table
from database import meta, engine

QuoteInDb = Table('quote', meta, autoload=True,
                  autoload_with=engine)

QuoteCommentInDb = Table('quotecomment', meta, autoload=True,
                         autoload_with=engine)
