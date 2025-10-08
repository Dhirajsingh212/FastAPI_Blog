from db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)


class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    Description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
