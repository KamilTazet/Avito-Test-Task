
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