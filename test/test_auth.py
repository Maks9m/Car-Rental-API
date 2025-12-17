# test/test_auth.py
from fastapi import status

def test_register_user(client):
    """Тест: Чи працює створення юзера і ліцензії"""
    payload = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "firstname": "John",
        "lastname": "Doe",
        "driver_license": { "license_number": "ABC12345", "license_type": "B", "expiry_date": "2025-12-31" }
    }
    
    response = client.post("/users/register", json=payload)
    
    # Перевірка 1: Статус 201 Created
    assert response.status_code == status.HTTP_201_CREATED
    
    # Перевірка 2: Повернулись правильні дані (без пароля!)
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "user_id" in data
    assert "password" not in data

def test_login_and_get_token(client):
    """Тест: Реєструємось, потім логінимось і отримуємо токен"""
    # 1. Спочатку треба зареєструватись (база чиста перед кожним тестом)
    client.post("/users/register", json={
        "email": "user@example.com",
        "password": "mypassword",
        "firstname": "Test",
        "lastname": "User",
        "driver_license": {"license_number": "XYZ98765", "license_type": "B", "expiry_date": "2025-12-31"}
    })
    
    # 2. Пробуємо залогінитись (Form Data, не JSON!)
    login_data = {
        "username": "user@example.com", # OAuth2 очікує поле username
        "password": "mypassword"
    }
    
    response = client.post("/token", data=login_data)
    
    # Перевірка: Отримали токен
    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    assert token_data["access_token"]

def test_authorization_flow(client):
    """
    Повний цикл: 
    1. Реєстрація
    2. Логін -> Токен
    3. Доступ до захищеного ресурсу з токеном
    """
    # --- КРОК 1: Реєстрація ---
    client.post("/users/register", json={
        "email": "auth@test.com",
        "password": "secret_password", 
        "firstname": "Auth",
        "lastname": "Master",
        "driver_license": {"license_number": "AUTH001", "license_type": "B", "expiry_date": "2025-12-31"}
    })
    
    # --- КРОК 2: Логін ---
    login_res = client.post("/token", data={"username": "auth@test.com", "password": "secret_password"})
    
    token = login_res.json()["access_token"]
    
    # --- КРОК 3: Перевірка авторизації ---
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "auth@test.com"

def test_login_wrong_password(client):
    """Тест: Негативний сценарій - неправильний пароль"""
    # Реєстрація
    client.post("/users/register", json={
        "email": "wrong@test.com",
        "password": "correct_password",
        "firstname": "Test",
        "lastname": "User",
        "driver_license": {"license_number": "ERR001", "license_type": "B", "expiry_date": "2025-12-31"}
    })
    
    # Спроба входу з помилкою
    response = client.post("/token", data={
        "username": "wrong@test.com",
        "password": "WRONG_PASSWORD"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED