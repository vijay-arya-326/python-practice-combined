from src.auth_service import login

def test_login_success():
    result = login("user", "password")

    assert result["message"] == "Login successful"
    assert result["access_token"]
    assert result["token_type"] == "bearer"