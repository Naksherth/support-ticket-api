import pytest
from app import create_app
from app.extensions import db
from app.models import User, Ticket

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def register_user(client):
    def _register(username="testuser", email="test@example.com", password="testpass", role="user"):
        response = client.post("/auth/register", json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        })
        if response.status_code not in (201, 409):  
            print("Registration failed response JSON:", response.get_json())
        assert response.status_code in (201, 409), f"Registration failed: {response.get_data(as_text=True)}"
        return response
    return _register

@pytest.fixture
def login_user(client, register_user):
    def _login(username="testuser", email="test@example.com", password="testpass", role="user"):
        # Try login first
        response = client.post("/auth/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            token = response.get_json().get("access_token")
            assert token is not None, "No access_token in login response"
            return token

        # If login fails, register then login
        register_user(username, email, password, role)
        response = client.post("/auth/login", json={
            "username": username,
            "password": password
        })
        assert response.status_code == 200, f"Login failed after registration: {response.get_data(as_text=True)}"
        token = response.get_json().get("access_token")
        assert token is not None, "No access_token in login response"
        return token
    return _login
