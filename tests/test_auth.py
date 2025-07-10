import uuid

def test_register_and_login(client, register_user):
    unique_id = uuid.uuid4().hex[:6]
    username = f"testuser_{unique_id}"
    email = f"test{unique_id}@example.com"
    password = "testpass"

    # Register user successfully
    resp = register_user(username=username, email=email, password=password)
    assert resp.status_code == 201
    assert resp.json["msg"] == "User registered successfully"

    # Register user with missing fields (should fail)
    resp = client.post("/auth/register", json={"username": "a"})
    assert resp.status_code == 400

    # Register duplicate user (same username/email again)
    resp = register_user(username=username, email=email, password=password)
    assert resp.status_code == 409

    # Login success with correct credentials
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200
    assert "access_token" in resp.json

    # Login failure with wrong password
    resp = client.post("/auth/login", json={"username": username, "password": "wrong"})
    assert resp.status_code == 401
