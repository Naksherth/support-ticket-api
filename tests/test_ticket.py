def test_create_and_get_tickets(client, login_user):
    token = login_user()

    # Create a ticket with valid description length (≥10 chars)
    resp = client.post("/tickets", json={
        "title": "Issue 1",
        "description": "Detailed description here",  # >=10 chars
        "priority": "high"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)
    data = resp.get_json()
    assert data["title"] == "Issue 1"
    ticket_id = data["id"]

    # Get tickets for the logged-in user (should include created ticket)
    resp = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    tickets = resp.get_json()
    assert isinstance(tickets, list)
    assert any(t["id"] == ticket_id for t in tickets)


def test_update_ticket(client, login_user):
    token = login_user()

    # Create a ticket with valid description length
    resp = client.post("/tickets", json={
        "title": "Old Title",
        "description": "A valid old description"  # >=10 chars
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)
    ticket_id = resp.get_json()["id"]

    # Update ticket title and status
    resp = client.put(f"/tickets/{ticket_id}", json={
        "title": "New Title",
        "status": "closed"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Ticket updated successfully"


def test_delete_ticket_forbidden(client, login_user, register_user):
    # Create admin user and login (unique credentials)
    register_user("adminuser", "adminuser@example.com", "adminpass", role="admin")
    admin_token = login_user("adminuser", "adminuser@example.com", "adminpass")

    # Create user1 and user2 with unique credentials
    register_user("user1", "user1@example.com", "password1", role="user")
    user1_token = login_user("user1", "user1@example.com", "password1")

    register_user("user2", "user2@example.com", "password2", role="user")
    user2_token = login_user("user2", "user2@example.com", "password2")

    # user1 creates a ticket with valid description length
    resp = client.post("/tickets", json={
        "title": "User1's ticket",
        "description": "This is a valid description." 
    }, headers={"Authorization": f"Bearer {user1_token}"})
    assert resp.status_code == 201, resp.get_data(as_text=True)
    ticket_id = resp.get_json()["id"]

    # user2 tries to delete user1's ticket (should be forbidden)
    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {user2_token}"})
    assert resp.status_code == 403
    assert "msg" in resp.get_json()
    assert resp.get_json()["msg"].startswith("Forbidden")

    # admin deletes user1's ticket (should succeed)
    resp = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert resp.get_json()["msg"].startswith("Ticket deleted successfully")
