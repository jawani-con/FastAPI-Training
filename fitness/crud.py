from sqlalchemy.orm import Session
from fitness.models import Fitness, MembershipDetails as DBMembershipDetails  # SQLAlchemy model import
from fitness.schemas import FitnessBase, MembershipDetails as PydanticMembershipDetails  # Pydantic schema import

# Function to delete a user by username
def delete_fitness_by_username(db: Session, username: str):
    user = db.query(Fitness).filter(Fitness.username == username).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# Function to create a new Fitness user
def create_fitness(db: Session, fitness: FitnessBase):
    db_fitness = Fitness(
        username=fitness.username, 
        password=fitness.password, 
        role=fitness.role
    )
    db.add(db_fitness)
    db.commit()
    db.refresh(db_fitness)
    return db_fitness

# Function to create membership details for a user
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

# Function to get a Fitness user by user ID
def get_fitness(db: Session, user_id: int):
    return db.query(Fitness).filter(Fitness.id == user_id).first()

# Function to get a Fitness user by username
def get_fitness_by_username(db: Session, username: str):
    return db.query(Fitness).filter(Fitness.username == username).first()

def get_all_members(db: Session):
    return db.query(Fitness).all()
