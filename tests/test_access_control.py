import pytest
import uuid

def test_user_cannot_update_others_ticket(client, login_user, register_user):
    unique_id = uuid.uuid4().hex[:6]
    userA_name = f"userA_{unique_id}"
    userA_email = f"a{unique_id}@example.com"
    userB_name = f"userB_{unique_id}"
    userB_email = f"b{unique_id}@example.com"

    register_user(userA_name, userA_email, "passwordA", role="user")
    userA_token = login_user(userA_name, userA_email, "passwordA")

    register_user(userB_name, userB_email, "passwordB", role="user")
    userB_token = login_user(userB_name, userB_email, "passwordB")

    resp = client.post("/tickets", json={
        "title": "UserA Ticket",
        "description": "Details for A's ticket - valid length"
    }, headers={"Authorization": f"Bearer {userA_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    resp = client.put(f"/tickets/{ticket_id}", json={
        "title": "Malicious update attempt"
    }, headers={"Authorization": f"Bearer {userB_token}"})

    assert resp.status_code == 403
    assert "msg" in resp.get_json()
    assert resp.get_json()["msg"].startswith("Forbidden")


def test_admin_can_update_any_ticket(client, login_user, register_user):
    unique_id = uuid.uuid4().hex[:6]
    admin_name = f"adminuser_{unique_id}"
    admin_email = f"admin{unique_id}@example.com"
    user_name = f"normaluser_{unique_id}"
    user_email = f"user{unique_id}@example.com"

    register_user(admin_name, admin_email, "adminpass", role="admin")
    admin_token = login_user(admin_name, admin_email, "adminpass")

    register_user(user_name, user_email, "userpass", role="user")
    user_token = login_user(user_name, user_email, "userpass")

    resp = client.post("/tickets", json={
        "title": "User Ticket",
        "description": "Description with enough length."
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    resp = client.put(f"/tickets/{ticket_id}", json={
        "status": "closed"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Ticket updated successfully"


def test_create_and_get_tickets(client, login_user):
    unique_id = uuid.uuid4().hex[:6]
    username = f"user_{unique_id}"
    email = f"user{unique_id}@example.com"
    token = login_user(username, email, "testpass")

    resp = client.post("/tickets", json={
        "title": "Issue 1",
        "description": "Detailed issue description here.",
        "priority": "high"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_data = resp.get_json()
    assert ticket_data["title"] == "Issue 1"
    ticket_id = ticket_data["id"]

    resp = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    tickets = resp.get_json()
    assert isinstance(tickets, list)
    assert any(t["id"] == ticket_id for t in tickets)


def test_update_ticket(client, login_user):
    unique_id = uuid.uuid4().hex[:6]
    username = f"user_{unique_id}"
    email = f"user{unique_id}@example.com"
    token = login_user(username, email, "testpass")

    resp = client.post("/tickets", json={
        "title": "Old Title",
        "description": "A valid old description text."
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    resp = client.put(f"/tickets/{ticket_id}", json={
        "title": "New Title",
        "status": "closed"
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Ticket updated successfully"


def test_delete_ticket_forbidden(client, login_user, register_user):
    unique_id = uuid.uuid4().hex[:6]
    admin_name = f"adminuser_{unique_id}"
    admin_email = f"admin{unique_id}@example.com"
    user1_name = f"user1_{unique_id}"
    user1_email = f"user1_{unique_id}@example.com"
    user2_name = f"user2_{unique_id}"
    user2_email = f"user2_{unique_id}@example.com"

    register_user(admin_name, admin_email, "adminpass", role="admin")
    admin_token = login_user(admin_name, admin_email, "adminpass")

    register_user(user1_name, user1_email, "password1", role="user")
    user1_token = login_user(user1_name, user1_email, "password1")

    register_user(user2_name, user2_email, "password2", role="user")
    user2_token = login_user(user2_name, user2_email, "password2")

    resp = client.post("/tickets", json={
        "title": "User1's ticket",
        "description": "This is a valid description."
    }, headers={"Authorization": f"Bearer {user1_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {user2_token}"})
    assert resp.status_code == 403
    assert "msg" in resp.get_json()
    assert resp.get_json()["msg"].startswith("Forbidden")

    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert resp.get_json()["msg"].startswith("Ticket deleted successfully")
