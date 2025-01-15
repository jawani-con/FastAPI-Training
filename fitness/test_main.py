from fastapi.testclient import TestClient
from fitness.main import app  
from fitness.routers.fitness import router
from unittest.mock import MagicMock
from fitness.auth.oauth2 import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Mock get_current_user for tests that require authentication
mock_user_admin = MagicMock(return_value={"id": 1, "username": "admin", "role": "admin"})
mock_user_user = MagicMock(return_value={"id": 2, "username": "user", "role": "user"})


# Test Cases

def test_login_success():
    response = client.post("/login", json={"username": "valid_user", "password": "valid_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure():
    response = client.post("/login", json={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_register_success():
    response = client.post("/register", json={"username": "new_user", "password": "new_password", "role": "user"})
    assert response.status_code == 200
    assert response.json()["response"] == "user registered"


def test_register_failure_user_exists():
    response = client.post("/register", json={"username": "existing_user", "password": "password", "role": "user"})
    assert response.status_code == 401
    assert response.json()["detail"] == "User exists"


def test_view_all_members():
    app.dependency_overrides[get_current_user] = mock_user_admin
    response = client.get("/admin/members")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of members
    app.dependency_overrides = {}


def test_delete_user_success():
    app.dependency_overrides[get_current_user] = mock_user_admin
    response = client.delete("/admin/members/delete/test_user")
    assert response.status_code == 200
    assert response.json()["message"] == "User test_user deleted successfully"
    app.dependency_overrides = {}


def test_delete_user_failure():
    app.dependency_overrides[get_current_user] = mock_user_admin
    response = client.delete("/admin/members/delete/nonexistent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    app.dependency_overrides = {}


def test_view_membership_details_user():
    app.dependency_overrides[get_current_user] = mock_user_user
    response = client.get("/members")
    assert response.status_code == 200
    app.dependency_overrides = {}


def test_view_membership_details_forbidden():
    app.dependency_overrides[get_current_user] = mock_user_admin
    response = client.get("/members")
    assert response.status_code == 403
    assert response.json()["detail"] == "Access forbidden for admin"
    app.dependency_overrides = {}


def test_renew_membership_success():
    app.dependency_overrides[get_current_user] = mock_user_user
    response = client.post("/members/renew")
    assert response.status_code == 200
    app.dependency_overrides = {}


def test_renew_membership_forbidden():
    app.dependency_overrides[get_current_user] = mock_user_admin
    response = client.post("/members/renew")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admins cannot renew memberships"
    app.dependency_overrides = {}
