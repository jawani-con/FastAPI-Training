from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from fitness.crud import get_fitness_by_username
from fitness.database import get_db
from fitness.schemas import Token, TokenData
from fitness.auth.token import verify_token, create_access_token
from fitness.auth.hashing import verify_password  

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
# router=APIRouter()

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = get_fitness_by_username(db, username=form_data.username)
#     if not user or not verify_password(form_data.password, user.password):  # Correct the password verification
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = verify_token(token)
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
    
#     user = get_fitness_by_username(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from fitness.crud import get_fitness_by_username
# from fitness.database import get_db
# from fitness.auth.token import create_access_token
# from fitness.auth.hashing import verify_password
# from fitness.schemas import Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Define a custom Pydantic model for the login request
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_fitness_by_username(db, username=data.username)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_fitness_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
