from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..models import Vote
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import Vote
from ..oauth2 import get_current_user
from typing import Optional


router = APIRouter(prefix='/votes', tags=['Votes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def set_vote(
        vote: Vote, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    my_vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == user_id)
    my_vote = my_vote_query.first()
    if vote.dir == 1:
        if my_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {user_id} has already voted')
        new_vote = Vote(**vote.dict())
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {'message': 'Success Voted'}
    else:
        if not my_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Exist')
        my_vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Success Deleted Vote'}
