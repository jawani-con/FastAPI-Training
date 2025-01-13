from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fitness.database import get_db
from fitness.crud import get_fitness, create_fitness, create_membership_details, get_fitness_by_username, delete_fitness_by_username
from fitness.schemas import FitnessBase, MembershipDetails, Fitness
from fitness.models import UserRole

router = APIRouter()

@router.post("/admin/members/", response_model=Fitness, status_code=status.HTTP_201_CREATED)
def create_fitness_user(fitness: FitnessBase, db: Session = Depends(get_db)):
    db_user = get_fitness_by_username(db, username=fitness.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return create_fitness(db, fitness=fitness)

# @router.post("/admin/members/membership/{user_id}/", status_code=status.HTTP_201_CREATED)
# def create_membership(user_id: int, membership: MembershipDetails, db: Session = Depends(get_db)):
#     return create_membership_details(db, membership_details=membership, user_id=user_id)

@router.post("/admin/members/membership/{user_id}/", status_code=status.HTTP_201_CREATED)
def create_membership(user_id: int, membership: MembershipDetails, db: Session = Depends(get_db)):
    user = get_fitness(db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role == UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin can't have membership")
    
    return create_membership_details(db, membership_details=membership, user_id=user_id)


@router.delete("/admin/members/delete/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    user = delete_fitness_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {username} deleted successfully"}