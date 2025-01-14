from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from fitness.crud import get_fitness_by_username, create_fitness
from fitness.database import get_db
from fitness.schemas import Token, TokenData, FitnessBase
from fitness.auth.token import verify_token, create_access_token
from fitness.auth.hashing import verify_password  
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

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


@router.post("/register")
def register(fitness: FitnessBase, db: Session = Depends(get_db)):
    user = get_fitness_by_username(db, username=fitness.username)
    if not user:
        create_fitness(db, fitness=fitness)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # access_token = create_access_token(data={"sub": user.username})
    return {"response":"user registered"}


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
