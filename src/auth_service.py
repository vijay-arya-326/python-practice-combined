import datetime
import os
import jwt

# In a real application, this secret key should be stored securely (e.g., environment variable)
# and be much more complex.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    to_encode = data.copy()
    # Add expiration time
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(username, password):
    # In a real application, you would verify the username and password against a database
    if username == "user" and password == "password":
        # If authentication is successful, create a JWT token
        token_data = {"sub": username, "role": "user"}
        jwt_token = create_jwt_token(token_data)
        return {"message": "Login successful", "access_token": jwt_token, "token_type": "bearer"}
    else:
        return {"message": "Invalid credentials"}

# Example usage:
print(login("user", "password"))
# print(login("wrong_user", "wrong_password"))