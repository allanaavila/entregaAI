from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///logistica.db")


def get_engine():
    return create_engine(DATABASE_URL)

 
def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()


# database/init_db.py
def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)