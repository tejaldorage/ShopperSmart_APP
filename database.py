from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./shopsmart.db"

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False})

sessionlocal = sessionmaker(bind=engine, autoflush= False, autocommit = False)
SessionLocal = sessionlocal

Base = declarative_base()