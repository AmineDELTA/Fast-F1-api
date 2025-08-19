from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

import os

env_file= ".env.local" if os.path.exists(".env.local") else ".env"
load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Missing DATABASE_URL in .env file")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_table():
    Base.metadata.create_all(bind=engine)
