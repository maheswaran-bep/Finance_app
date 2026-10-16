
from uuid import uuid4

from fastapi.testclient import TestClient
from backend.routers.users import router

client = TestClient(router)


def test_register_user():
    unique_id = int(uuid4().int % 2_000_000_000) + 1

    user_data = {
        "id_": unique_id,
        "username": f"test_user_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "testpassword",
    }

    response = client.post("/users/register", json=user_data)

    assert response.status_code == 200
    assert response.json()["msg"] == "register successfuly"



def test_reset_password(monkeypatch):
    email_data = {"Email": "test@example.com"}

    # Mock email delivery so the test doesn't connect to Gmail.
    monkeypatch.setattr(
        "backend.core.forgot_pass.send_email",
        lambda *args, **kwargs: None,
    )

    response = client.post(
        "/users/reset_password",
        json=email_data,
    )

    assert response.status_code == 200
    assert "message" in response.json()

