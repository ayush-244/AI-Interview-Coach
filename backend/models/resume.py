from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from database.db import engine

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    resume_text = Column(Text)

Base.metadata.create_all(bind=engine)