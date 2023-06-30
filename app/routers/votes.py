from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/votes', tags=['Votes']
)


# Add a vote
@router.post('/', status_code=status.HTTP_201_CREATED)
def add_vote(vote: schemas.Vote,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):

    # Post or user idempotence
    query_instance = db.query(models.PostServerData).filter(models.PostServerData.id == vote.post_id)
    is_posted = query_instance.first()
    if not is_posted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} does not exist')

    # Voting logic
    vote_query_instance = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                                  models.Vote.user_id == current_user.user_id)
    has_voted = vote_query_instance.first()

    if vote.direction == 1:
        if has_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.user_id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.user_id)
        db.add(new_vote)
        db.commit()

        return {'message': 'Vote added successfully'}
    else:
        if not has_voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Vote does not exist')
        vote_query_instance.delete(synchronize_session=False)
        db.commit()

        return {'message': 'Vote deleted successfully'}
