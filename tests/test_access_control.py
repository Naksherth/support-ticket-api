def test_user_cannot_update_others_ticket(client, login_user, register_user):
    # Use passwords with at least 6 chars
    register_user("userA", "a@example.com", "passwordA", role="user")
    userA_token = login_user("userA", "a@example.com", "passwordA")

    register_user("userB", "b@example.com", "passwordB", role="user")
    userB_token = login_user("userB", "b@example.com", "passwordB")

    # UserA creates a ticket with valid description length (>=10 chars)
    resp = client.post("/tickets", json={
        "title": "UserA Ticket",
        "description": "Details for A's ticket - valid length"
    }, headers={"Authorization": f"Bearer {userA_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_data = resp.get_json()
    ticket_id = ticket_data["id"]

    # UserB attempts to update UserA's ticket - should be forbidden
    resp = client.put(f"/tickets/{ticket_id}", json={
        "title": "Malicious update attempt"
    }, headers={"Authorization": f"Bearer {userB_token}"})

    assert resp.status_code == 403
    assert "msg" in resp.get_json()
    assert resp.get_json()["msg"].startswith("Forbidden")


def test_admin_can_update_any_ticket(client, login_user, register_user):
    # Ensure unique user data for admin and user
    register_user("adminuser", "adminuser@example.com", "adminpass", role="admin") 
    admin_token = login_user("adminuser", "adminuser@example.com", "adminpass")

    register_user("normaluser", "normaluser@example.com", "userpass", role="user")
    user_token = login_user("normaluser", "normaluser@example.com", "userpass")

    # Normal user creates a ticket with valid description length
    resp = client.post("/tickets", json={
        "title": "User Ticket",
        "description": "Description with enough length."
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_data = resp.get_json()
    ticket_id = ticket_data["id"]

    # Admin updates the ticket's status
    resp = client.put(f"/tickets/{ticket_id}", json={
        "status": "closed"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["msg"] == "Ticket updated successfully"
    # You can optionally check ticket ID if returned
    # assert data.get("id") == ticket_id  # Only if your API returns it


def test_create_and_get_tickets(client, login_user):
    token = login_user()

    # Create a valid ticket
    resp = client.post("/tickets", json={
        "title": "Issue 1",
        "description": "Detailed issue description here.",
        "priority": "high"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_data = resp.get_json()
    assert ticket_data["title"] == "Issue 1"
    ticket_id = ticket_data["id"]

    # Get tickets for the user
    resp = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    tickets = resp.get_json()
    assert isinstance(tickets, list)
    assert any(t["id"] == ticket_id for t in tickets)


def test_update_ticket(client, login_user):
    token = login_user()

    # Create a valid ticket
    resp = client.post("/tickets", json={
        "title": "Old Title",
        "description": "A valid old description text."
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    # Update the ticket
    resp = client.put(f"/tickets/{ticket_id}", json={
        "title": "New Title",
        "status": "closed"
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Ticket updated successfully"


def test_delete_ticket_forbidden(client, login_user, register_user):
    # Use unique user data for admin and normal users
    register_user("adminuser", "adminuser@example.com", "adminpass", role="admin") 
    admin_token = login_user("adminuser", "adminuser@example.com", "adminpass")

    register_user("user1", "user1@example.com", "password1", role="user")
    user1_token = login_user("user1", "user1@example.com", "password1")

    register_user("user2", "user2@example.com", "password2", role="user")
    user2_token = login_user("user2", "user2@example.com", "password2")

    # User1 creates a ticket
    resp = client.post("/tickets", json={
        "title": "User1's ticket",
        "description": "This is a valid description."
    }, headers={"Authorization": f"Bearer {user1_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)

    ticket_id = resp.get_json()["id"]

    # User2 tries to delete User1's ticket - should be forbidden
    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {user2_token}"})
    assert resp.status_code == 403
    assert "msg" in resp.get_json()
    assert resp.get_json()["msg"].startswith("Forbidden")

    # Admin deletes the ticket - should succeed
    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert resp.get_json()["msg"].startswith("Ticket deleted successfully")
