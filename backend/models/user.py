from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database.db import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))

Base.metadata.create_all(bind=engine)