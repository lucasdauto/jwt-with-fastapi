from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy.exc import IntegrityError
from app.database.models import UserModel
from app.schemas import User
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from decouple import config


crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRETE_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

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
    
    def user_login(self, user: User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRETE_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }
