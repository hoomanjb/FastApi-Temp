from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from .models import Post, User
from .database import engine, get_db, Base
from sqlalchemy.orm import Session
from typing import List

from .schemas import PostCreate, PostResponse, UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


# /docs - /redoc
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(post_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.id == post_id).all()
    return {'detail': posts}


@app.get("/posts/{id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found"
        )
    return {'detail': post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content, published=post.published)
    # new_post = Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    my_post = db.query(Post).filter(Post.id == post_id)
    pre_post = my_post.first()
    if pre_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")

    my_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'post updated'}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'data': new_user}
