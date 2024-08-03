from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE = create_engine(os.getenv('DATABASE'), connect_args={'check_same_thread': False})

SESSION = sessionmaker(bind=DATABASE)
session = SESSION()

BASE = declarative_base()

def create_db():
    BASE.metadata.create_all(DATABASE)

def drop_db():
    BASE.metadata.drop_all(DATABASE)