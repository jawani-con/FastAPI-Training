from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fitness.database import get_db
from fitness.crud import get_fitness, create_fitness, create_membership_details, get_fitness_by_username, delete_fitness_by_username, get_all_members, get_membership_details, renew_membership
from fitness.schemas import FitnessBase, MembershipDetails, Fitness
from fitness.models import UserRole
from typing import List
from fitness.schemas import MemberResponse
from fitness.auth.oauth2 import get_current_user

router = APIRouter()

@router.post("/admin/members/", response_model=Fitness, status_code=status.HTTP_201_CREATED)
def create_fitness_user(fitness: FitnessBase, db: Session = Depends(get_db)):
    db_user = get_fitness_by_username(db, username=fitness.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return create_fitness(db, fitness=fitness)

@router.post("/admin/members/{user_id}/", status_code=status.HTTP_201_CREATED)
def create_membership(user_id: int, membership: MembershipDetails, db: Session = Depends(get_db)):
    user = get_fitness(db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role == UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin logged in")
    
    return create_membership_details(db, membership_details=membership, user_id=user_id)


@router.delete("/admin/members/delete/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    user = delete_fitness_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {username} deleted successfully"}

@router.get("/admin/members", response_model=List[MemberResponse])
def view_all_members(db: Session = Depends(get_db)):
    members = get_all_members(db)
    return members

@router.get("/members", response_model=MembershipDetails)
def view_membership_details(current_user: Fitness = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden for admin")

    membership = get_membership_details(db, user_id=current_user.id)

    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership details not found")

    return membership

@router.post("/members/renew", response_model=MembershipDetails)
def renew_membership_endpoint(current_user: Fitness = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins cannot renew memberships")

    membership = renew_membership(db, user_id=current_user.id)

    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership details not found")

    return membership
