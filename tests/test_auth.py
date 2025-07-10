def test_register_and_login(client, register_user):
    # Test registration success
    resp = register_user()
    assert resp.status_code == 201
    assert resp.json["msg"] == "User registered successfully"

    # Register user with missing fields
    resp = client.post("/auth/register", json={"username": "a"})
    assert resp.status_code == 400

    # Register duplicate user
    resp = register_user()
    assert resp.status_code == 409

    # Login success
    resp = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    assert resp.status_code == 200
    assert "access_token" in resp.json

    # Login failure (wrong password)
    resp = client.post("/auth/login", json={"username": "testuser", "password": "wrong"})
    assert resp.status_code == 401
