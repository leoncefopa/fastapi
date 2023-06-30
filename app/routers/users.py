from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix='/users', tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user_payload: schemas.UserDefault, db: Session = Depends(get_db)):
    # Hashing the password
    hashed_password = utils.hashing(user_payload.password)
    user_payload.password = hashed_password

    new_user = models.User(**user_payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=schemas.UserOutput)
def get_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} does not exist')
    return user

