from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..models import Post, User
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import UserLogin, PostResponse
from ..utils import hashing, verify


router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    my_user = db.query(User).filter(User.email == user.email).first()

    if not my_user or not verify(user.password, my_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user.email} Not found"
        )

    return {'token': 'example token'}
