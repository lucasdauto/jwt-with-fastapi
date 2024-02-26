from sqlalchemy import Column, Integer, String
from app.database.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column('id',Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    username = Column('username',String)
    email = Column('email',String)
    password = Column('password',String)
