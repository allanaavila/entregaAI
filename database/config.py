from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///entregaAI.db")

def get_engine():
    return create_engine(DATABASE_URL)

def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()
