from fastapi import status, HTTPException, Depends, APIRouter
from ..models import User
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserResponse
from ..utils import hashing


router = APIRouter(prefix='/users')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    user.password = hashing(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
