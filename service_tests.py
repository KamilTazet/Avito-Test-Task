import pytest
from fastapi.testclient import TestClient
from service import app
# from app.schemas import AuthRequest, SendCoinRequest
from schemas import *

client = TestClient(app)

# Тест аутентификации
@pytest.fixture
def valid_user():
    return {"username": "Ivan", "password": "11111"}

# Тест на создание и аутентификацию пользователя
def test_authenticate(valid_user):
    response = client.post("/api/auth", json=valid_user)
    assert response.status_code == 200
    assert "token" in response.json()

# Тест на получение информации о пользователе
def test_get_info(valid_user):
    # Сначала аутентифицируемся, получаем токен
    auth_response = client.post("/api/auth", json=valid_user)
    token = auth_response.json()["token"]

    # Делаем запрос с токеном
    response = client.get(
        "/api/info", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "coins" in response.json()
    assert "inventory" in response.json()

# Тест на отправку коинов
def test_send_coin(valid_user):
    # Получаем токен для авторизации
    auth_response = client.post("/api/auth", json=valid_user)
    token = auth_response.json()["token"]

    # Отправляем коины
    send_coin_data = {"toUser": "Ruslan", "amount": 50}
    response = client.post(
        "/api/sendCoin",
        headers={"Authorization": f"Bearer {token}"},
        json=send_coin_data
    )
    assert response.status_code == 200
    assert response.json() == {"description": "Успешный ответ."}

# Тест на покупку мерча
def test_buy_item(valid_user):
    # Получаем токен для авторизации
    auth_response = client.post("/api/auth", json=valid_user)
    token = auth_response.json()["token"]

    # Покупаем мерч
    response = client.get(
        "/api/buy/powerbank", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"description": "Успешный ответ."}

# Пример теста на ошибку
def test_send_coin_not_enough_balance(valid_user):
    # Получаем токен для авторизации
    auth_response = client.post("/api/auth", json=valid_user)
    token = auth_response.json()["token"]

    # Отправляем коинов больше чем есть
    send_coin_data = {"toUser": "Ruslan", "amount": 10000}  # Примерно больше чем у пользователя
    response = client.post(
        "/api/sendCoin",
        headers={"Authorization": f"Bearer {token}"},
        json=send_coin_data
    )
    assert response.status_code == 400  # Ожидаем ошибку из-за недостаточного баланса