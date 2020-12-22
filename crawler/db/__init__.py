from sqlalchemy.orm import sessionmaker

from .models import Base, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
