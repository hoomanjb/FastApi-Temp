from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret-key -> openssl.exe rand -hex 32
# algorithm , expriation time

SECRET_KEY = '118af103d8dd70d2b3c0b8ac38d6de6b7efe04feee2e6629793ce35d48c7ebe8'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire_datetime = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_datetime})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
