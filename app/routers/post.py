from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..models import Post, Vote
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import PostCreate, PostResponse
from ..oauth2 import get_current_user
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get("/", response_model=List[PostResponse])
async def get_posts(
        post_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(Post).filter(Post.id == post_id).filter(
        Post.user_id == user_id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(Post, func.count(Vote.post_id).label('votes')).join(
        Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).filter(
        Post.title.contains(search)).limit(limit).offset(skip).all()

    return {'detail': posts}


@router.get("/{id}", response_model=PostResponse)
async def get_post(
        post_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found"
        )
    if user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    return {'detail': post}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(
        post: PostCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, published=post.published, user_id=user_id)
    # new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")
    if user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_post(
        post_id: int, post: PostCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    my_post = db.query(Post).filter(Post.id == post_id)
    pre_post = my_post.first()
    if pre_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} Not found")
    if user_id != pre_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    my_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'post updated'}
