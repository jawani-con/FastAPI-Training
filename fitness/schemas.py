# from pydantic import BaseModel, model_validator
# from typing import Optional
# from datetime import date
# import enum

# class UserRole(str, enum.Enum):
#     user = "user"
#     admin = "admin"

# class MembershipDetails(BaseModel):
#     membership_date: date
#     membership_time: str

# class MembershipDetailss(MembershipDetails):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True

# class FitnessBase(BaseModel):
#     username: str
#     role: UserRole
#     password: str

# class Fitness(FitnessBase):
#     id: int
#     membership_details: Optional[MembershipDetails] = None

#     @model_validator(mode='before')
#     def set_membership_details(cls, values):
#         if values.get("role") == UserRole.USER and values.get("membership_details") is None:
#             values["membership_details"] = None  
#         return values

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str

from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class MembershipDetails(BaseModel):
    membership_date: date
    membership_time: str

class FitnessBase(BaseModel):
    username: str
    role: UserRole
    password: str

class Fitness(FitnessBase):
    id: int
    membership_details: Optional[MembershipDetails] = None

    @model_validator(mode='before')
    def set_membership_details(cls, values):
        if values.get("role") == UserRole.admin and values.get("membership_details") is None:
            raise ValueError("Admin can't have membership details.")
        return values

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
