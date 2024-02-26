from fastapi import APIRouter, Depends, Response
from app.auth_user import UserCases
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.schemas import User

router = APIRouter(prefix= '/user')
router.include_router(UserCases.as_router())

@router.post('/register')
def user_register(
        user: User,
        db_session: Session = Depends(get_db_session), 
    ):
    user = UserCases(db_session=db_session).user_register(user=user)

    return Response(
        content={"msg": "success"},  
        status_code=status.HTTP_201_CREATED
    )