from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy.exc import IntegrityError
from app.database.models import UserModel
from app.schemas import User
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException


cryt_context = CryptContext(schemes=['sha256_crypt'])

class UserCases:
    
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def user_register(self, user: User):
        try:
            new_user = UserModel(username=user.username, email=user.email, password=cryt_context.hash(user.password))
            self.db_session.add(new_user)
            self.db_session.commit()

            return new_user

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
            