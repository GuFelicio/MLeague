from sqlalchemy import Column, Integer, String
from Back.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    puuid = Column(String, unique=True, index=True)
