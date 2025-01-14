# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from fitness.database import Base, get_db
# from fitness.main import app
# from fitness.models import Fitness, MembershipDetails, UserRole

# # Create a test database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Override the dependency
# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)

# app.dependency_overrides[get_db] = lambda: next(test_db())

# client = TestClient(app)

# def create_test_user(db, username="testuser", role="user"):
#     user = Fitness(username=username, role=role, hashed_password="hashedpassword")
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# def test_create_fitness_user(test_db):
#     response = client.post(
#         "/admin/members/",
#         json={"username": "newuser", "role": "user", "password": "password123"},
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["username"] == "newuser"


# def test_duplicate_user_error(test_db):
#     create_test_user(test_db, username="existinguser")
#     response = client.post(
#         "/admin/members/",
#         json={"username": "existinguser", "role": "user", "password": "password123"},
#     )
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Username already registered"

# def test_create_membership(test_db):
#     user = create_test_user(test_db, username="membershipuser")
#     response = client.post(
#         f"/admin/members/{user.id}/",
#         json={"plan": "gold", "expiry_date": "2025-12-31"},
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["plan"] == "gold"


# def test_delete_user(test_db):
#     user = create_test_user(test_db, username="deleteuser")
#     response = client.delete(f"/admin/members/delete/{user.username}")
#     assert response.status_code == 200
#     assert response.json()["message"] == f"User {user.username} deleted successfully"


# def test_view_all_members(test_db):
#     create_test_user(test_db, username="member1")
#     create_test_user(test_db, username="member2")
#     response = client.get("/admin/members")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) >= 2


# def test_view_membership_details(test_db):
#     user = create_test_user(test_db, username="detailuser")
#     membership = MembershipDetails(plan="silver", expiry_date="2025-01-01", user_id=user.id)
#     test_db.add(membership)
#     test_db.commit()

#     response = client.get("/members", headers={"Authorization": f"Bearer {user.id}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["plan"] == "silver"


# def test_renew_membership(test_db):
#     user = create_test_user(test_db, username="renewuser")
#     membership = MembershipDetails(plan="gold", expiry_date="2025-01-01", user_id=user.id)
#     test_db.add(membership)
#     test_db.commit()

#     response = client.post("/members/renew", headers={"Authorization": f"Bearer {user.id}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["plan"] == "gold"
