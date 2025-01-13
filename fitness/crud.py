from sqlalchemy.orm import Session
from fitness.models import Fitness, MembershipDetails
from fitness.schemas import FitnessBase, MembershipDetails

def create_fitness(db: Session, fitness: FitnessBase):
    db_fitness = Fitness(username=fitness.username, password=fitness.password, role=fitness.role)
    db.add(db_fitness)
    db.commit()
    db.refresh(db_fitness)
    return db_fitness

def create_membership_details(db: Session, membership_details: MembershipDetails, user_id: int):
    db_membership = MembershipDetails(**membership_details.dict(), user_id=user_id)
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

def get_fitness(db: Session, user_id: int):
    return db.query(Fitness).filter(Fitness.id == user_id).first()

def get_fitness_by_username(db: Session, username: str):
    return db.query(Fitness).filter(Fitness.username == username).first()
