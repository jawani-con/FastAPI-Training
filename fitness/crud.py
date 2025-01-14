from sqlalchemy.orm import Session
from fitness.models import Fitness, MembershipDetails as DBMembershipDetails  
from fitness.schemas import FitnessBase, MembershipDetails as PydanticMembershipDetails  
from datetime import timedelta
from fitness.auth.hashing import get_password_hash

def delete_fitness_by_username(db: Session, username: str):
    user = db.query(Fitness).filter(Fitness.username == username).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def create_fitness(db: Session, fitness: FitnessBase):
    db_fitness = Fitness(
        username=fitness.username, 
        password=get_password_hash(fitness.password), 
        role=fitness.role
    )
    db.add(db_fitness)
    db.commit()
    db.refresh(db_fitness)
    return db_fitness

def create_membership_details(db: Session, membership_details: PydanticMembershipDetails, user_id: int):
    db_membership = DBMembershipDetails(
        user_id=user_id,
        membership_date=membership_details.membership_date,
        membership_time=membership_details.membership_time
    )
    
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

def get_fitness(db: Session, user_id: int):
    return db.query(Fitness).filter(Fitness.id == user_id).first()

def get_fitness_by_username(db: Session, username: str):
    return db.query(Fitness).filter(Fitness.username == username).first()

def get_all_members(db: Session):
    return db.query(Fitness).all()

def get_membership_details(db: Session, user_id: int):
    return db.query(DBMembershipDetails).filter(DBMembershipDetails.user_id == user_id).first()

def renew_membership(db: Session, user_id: int):
    membership = db.query(DBMembershipDetails).filter(DBMembershipDetails.user_id == user_id).first()
    
    if membership:
        membership.membership_date += timedelta(days=365)  # Extend the membership by 1 year
        db.commit()
        db.refresh(membership)
    return membership