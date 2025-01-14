from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from fitness.database import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class Fitness(Base):
    __tablename__ = "fitness"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    membership_details = relationship("MembershipDetails", back_populates="user", uselist=False)

class MembershipDetails(Base):
    __tablename__ = "membership_details"

    id = Column(Integer, primary_key=True, index=True)
    membership_date = Column(Date, nullable=False)
    membership_time = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("fitness.id"), nullable=False)
    user = relationship("Fitness", back_populates="membership_details")
