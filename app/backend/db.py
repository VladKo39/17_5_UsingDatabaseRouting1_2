from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine=create_engine('sqlite:///taskmanager1.db',echo=True)
SessionLocal=sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass