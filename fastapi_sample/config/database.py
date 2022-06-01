from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str)

engine = create_engine(DATABASE_URL)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
