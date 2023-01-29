from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Secret-key -> openssl.exe rand -hex 32
# algorithm , expriation time
from app.schemas import TokenData

SECRET_KEY = '118af103d8dd70d2b3c0b8ac38d6de6b7efe04feee2e6629793ce35d48c7ebe8'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_datetime})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        users_id: str = payload.get('user_id')
        if users_id is None:
            raise credentials_exception
        token_data = TokenData(id=users_id)
    except JWTError as error:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return verify_access_token(token, credentials_exception)
