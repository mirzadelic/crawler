from sqlalchemy.orm import sessionmaker

from .models import Base, engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
