def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "12345678",
            "role": "passenger",
        },
    )

    assert response.status_code in [200, 201]