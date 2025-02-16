
from pydantic import BaseModel
from typing import Annotated


class InventoryItem(BaseModel):
    type: str
    quantity: int


class CoinReceiveItem(BaseModel):
    fromUser: str
    amount: int

class CoinSendItem(BaseModel):
    toUser: str
    amount: int


# class CoinHistory(BaseModel):
#     received: Annotated[list[CoinReceiveItem], "Имя пользователя, который отправил монеты."]
#     sent: Annotated[list[CoinSendItem], "Количество полученных монет."]

# class InfoResponse(BaseModel):
#     coins: Annotated[int, "Количество доступных монет."]
#     inventory: list[InventoryItem]
#     coinHistory: CoinHistory

# class ErrorResponse(BaseModel):
#     errors: Annotated[str, "Сообщение об ошибке, описывающее проблему."]

# class AuthRequest(BaseModel):
#     username: Annotated[str, "Имя пользователя для аутентификации."]
#     password: Annotated[str, "Пароль для аутентификации."]

# class AuthResponse(BaseModel):
#     token: Annotated[str, "JWT-токен для доступа к защищенным ресурсам."]

# class SendCoinRequest(BaseModel):
#     toUser: Annotated[str, "Имя пользователя, которому нужно отправить монеты."]
#     amount: Annotated[int, "Количество монет, которые необходимо отправить."]


class CoinHistory(BaseModel):
    received: list
    sent: list

class InfoResponse(BaseModel):
    coins: int
    inventory: list[InventoryItem]
    coinHistory: CoinHistory

class ErrorResponse(BaseModel):
    errors: str

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str

class SendCoinRequest(BaseModel):
    toUser: str
    amount: int