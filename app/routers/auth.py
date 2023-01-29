from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..models import Post, User
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import UserLogin, PostResponse
from ..utils import hashing, verify
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

# OAuth2PasswordRequestForm -> username , password  -> send it form data
@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    my_user = db.query(User).filter(User.email == user.username).first()
    if not my_user or not verify(user.password, my_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    access_token = create_access_token(data={'user_id': 1})
    return {'access_token': access_token, 'token_type': 'bearer'}

