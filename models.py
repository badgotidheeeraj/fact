from sqlalchemy import Column, Integer, String
from database import Base

class TeaModel(Base):
    __tablename__ = "teas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    origin = Column(String)
    email = Column(String)
    owner_id = Column(Integer, index=True)




class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)