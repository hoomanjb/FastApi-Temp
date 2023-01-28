from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from .models import Post
from .database import engine, get_db, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


class PostReq(BaseModel):
    title: str
    content: str
    rank: Optional[int] = None
    published: bool = True

# /docs - /redoc
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/{id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = True
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found"
        )
    return {'detail': post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: PostReq):
    # do something
    return {'data': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    # do something
    if post_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(post_id: int, post: PostReq):
    if post_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")
    return {'message': 'post updated'}
