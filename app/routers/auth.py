from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm returns { 'username' : value, 'password': value }
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # Check if user exists
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    # Check if passwords match
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid credentials')

    # Create token
    access_token = oauth2.create_access_token(data= {'user_id': user.user_id})
    return {'access_token': access_token, 'token_type': 'Bearer'}

