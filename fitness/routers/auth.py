from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fitness.auth.hashing import verify_password
from fitness.auth.token import create_access_token
from fitness.auth.oauth2 import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from fitness.crud import get_fitness_by_username
from fitness.database import get_db
from datetime import timedelta
from fitness.schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_fitness_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
