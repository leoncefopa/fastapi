from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy import func, select

router = APIRouter(
    prefix='/posts', tags=['Posts']
)


# Retrieve all posts
@router.get('/', response_model=List[schemas.PostVoteOutput])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = '',
              current_user: int = Depends(oauth2.get_current_user)):
    # query_instance = db.query(models.PostServerData)
    # posts = query_instance.all()
    # posts = query_instance.filter(models.PostServerData.title.contains(search)).limit(limit).offset(skip)

    votes_count_query = db.query(models.PostServerData, func.count(models.Vote.post_id).label('votes'))\
        .join(models.Vote, models.Vote.post_id == models.PostServerData.id, isouter=True)\
        .group_by(models.PostServerData.id)\
        .filter(models.PostServerData.title.contains(search)).limit(limit).offset(skip)\
        .all()
    # print(votes_count_query)
    output = [{'posts': a, 'votes': b} for a, b in votes_count_query]
    # Retrieve only user posts
    # posts = query_instance.filter(models.PostServerData.owner_id == current_user.user_id).all()
    return output


# Retrieve a post given its id
@router.get('/{post_id}', response_model=schemas.PostVoteOutput)
def get_post_by_id(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_instance = db.query(models.PostServerData)
    post = query_instance.filter(models.PostServerData.id == post_id).first()
    # Retrieve only one of the current user posts
    # post = query_instance.filter(models.PostServerData.id == current_user.user_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} was not found.")

    post_message, vote_count = db.query(models.PostServerData, func.count(models.Vote.post_id).label('votes'))\
        .join(models.Vote, models.Vote.post_id == models.PostServerData.id, isouter=True)\
        .group_by(models.PostServerData.id)\
        .first()
    output = {'posts': post_message, 'votes': vote_count}
    # print()
    # if post.owner_id != current_user.user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform the requested action.")

    return output


# Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBaseOutput)
def create_posts(payload: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    input_payload = payload.dict()
    post = models.PostServerData(**input_payload, owner_id=current_user.user_id)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


# Updating a post
@router.put("/{post_id}", response_model=schemas.PostBaseOutput)
def update_posts(post_id: int, payload: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    query_instance = db.query(models.PostServerData).filter(models.PostServerData.id == post_id)
    post = query_instance.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} was not found.")

    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action.")

    input_payload = payload.dict()
    query_instance.update(input_payload, synchronize_session=False)
    db.commit()

    return query_instance.first()


# Delete a post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_instance = db.query(models.PostServerData).filter(models.PostServerData.id == post_id)
    post = query_instance.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} was not found.")

    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action.")

    query_instance.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
