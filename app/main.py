from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from .models import Post, User
from .database import engine, get_db, Base
from sqlalchemy.orm import Session
from typing import List
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from .utils import hashing
from .routers import post, user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

# /docs - /redoc
@app.get("/")
async def root():
    return {"message": "Hello World"}
