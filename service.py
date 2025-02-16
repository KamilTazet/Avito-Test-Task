from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, Query, HTTPException, status
from fastapi.exceptions import RequestValidationError
from typing_extensions import Annotated
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from database import *
import schemas


SECRET_KEY = "8a5907a63cc5206a3d635cc0503e3defc851def105b3d8301684e47740305f54"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class User(BaseModel):
    user_login: str | None = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    user_auth_query = db.query(UserAuth).filter(UserAuth.user_login == username).first()
    if user_auth_query:
        username = user_auth_query.user_login
        hashed_password = user_auth_query.user_password
        return UserInDB(user_login=username,hashed_password=hashed_password)
    else:
        return None
    
def create_user(db, username, password):
    new_user_hashed_password = get_password_hash(password)
    new_user_auth = UserAuth(user_login = username, user_password = new_user_hashed_password)
    db.add(new_user_auth)   
    db.commit()

    new_user_auth_id = db.query(UserAuth).filter(UserAuth.user_login == username).first().user_id
    new_employee_info = EmployeeInfo(employee_id=new_user_auth_id, employee_name=username, coins=1000)
    db.add(new_employee_info) 
    db.commit()
    return UserInDB(hashed_password=new_user_hashed_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        # return False
        return create_user(db, username, password)
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db = next(get_db())
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user_data = User(user_login=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=user_data.user_login)
    if user is None:
        raise credentials_exception
    return user



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc) -> schemas.ErrorResponse:
    error_responce = schemas.ErrorResponse(errors='Неверный запрос.')
    return PlainTextResponse(str(error_responce.model_dump()), status_code=400)

@app.get("/api/info")
async def get_info(current_user: Annotated[User, Depends(get_current_user)]):
    db = next(get_db())
    current_employee_info_query_result = db.query(EmployeeInfo).filter(EmployeeInfo.employee_name == current_user.user_login).first()

    current_coin_amount = current_employee_info_query_result.coins

    employee_inventory_query = db.query(EmployeeInventory).filter(EmployeeInventory.employee_id == current_employee_info_query_result.employee_id)
    employee_inventory_list = []
    if employee_inventory_query.count() > 0:
        for row in employee_inventory_query:
            merch_query_result=db.query(Merch).filter(Merch.merch_id == row.item_type).first()
            if merch_query_result:
                employee_inventory_list.append(schemas.InventoryItem(type=merch_query_result.merch_name,quantity=row.item_quantity))
    

    coin_received_list = []
    coin_received_quer_result = db.query(CoinTransfer).filter(CoinTransfer.receiver_id == current_employee_info_query_result.employee_id)
    if coin_received_quer_result.count() > 0:
        for row in coin_received_quer_result:
            sender_employee_info_query_result = db.query(EmployeeInfo).filter(EmployeeInfo.employee_id == row.sender_id).first()
            if sender_employee_info_query_result:
                coin_received_list.append(schemas.CoinReceiveItem(fromUser=sender_employee_info_query_result.employee_name,amount=row.coins_send_amount))

    coin_sent_list = []
    coin_sent_quer_result = db.query(CoinTransfer).filter(CoinTransfer.sender_id == current_employee_info_query_result.employee_id)
    if coin_sent_quer_result.count() > 0:
        for row in coin_sent_quer_result:
            receiver_employee_info_query_result = db.query(EmployeeInfo).filter(EmployeeInfo.employee_id == row.receiver_id).first()
            if receiver_employee_info_query_result:
                coin_sent_list.append(schemas.CoinSendItem(toUser=receiver_employee_info_query_result.employee_name,amount=row.coins_send_amount))


    
    return schemas.InfoResponse(coins=current_coin_amount,inventory=employee_inventory_list,coinHistory=schemas.CoinHistory(received=coin_received_list,sent=coin_sent_list))

@app.post("/api/sendCoin")
async def give_coins(sendCoinRequest: schemas.SendCoinRequest, current_user: Annotated[User, Depends(get_current_user)]):
    db = next(get_db())
    current_employee_info_query_result = db.query(EmployeeInfo).filter(EmployeeInfo.employee_name == current_user.user_login).first()
    send_to_user_query_result = db.query(EmployeeInfo).filter(EmployeeInfo.employee_name == sendCoinRequest.toUser).first()
    if send_to_user_query_result:
        if current_employee_info_query_result.coins - sendCoinRequest.amount >= 0:
            new_coins_amount = current_employee_info_query_result.coins - sendCoinRequest.amount
            current_employee_info_query_result.coins = new_coins_amount
            new_coin_transfer_entry = CoinTransfer(sender_id=current_employee_info_query_result.employee_id,receiver_id=send_to_user_query_result.employee_id,coins_send_amount=sendCoinRequest.amount)
            db.add(new_coin_transfer_entry)
            db.commit()
            return {"description": "Успешный ответ."}

@app.get("/api/buy/{item}")
async def buy_item(item, current_user: Annotated[User, Depends(get_current_user)]):
    db = next(get_db())
    merch_query_results = db.query(Merch).filter(Merch.merch_name == item).first()
    if merch_query_results:
        merch_price = merch_query_results.merch_cost
        # user = get_current_user()
        employee_query_results = db.query(EmployeeInfo).filter(EmployeeInfo.employee_name == current_user.user_login).first()
        if employee_query_results:
            coin_amount = employee_query_results.coins
            if coin_amount - merch_price >= 0:
                employee_query_results.coins = coin_amount - merch_price
                employee_inventory_query = db.query(EmployeeInventory).filter(EmployeeInventory.employee_id == employee_query_results.employee_id and EmployeeInventory.item_type==merch_query_results.merch_id).first()
                if employee_inventory_query:
                    new_item_quantity = employee_inventory_query.item_quantity + 1
                    employee_inventory_query.item_quantity = new_item_quantity
                else:
                    new_item_entry = EmployeeInventory(employee_id=employee_query_results.employee_id,item_type=merch_query_results.merch_id,item_quantity=1)
                    db.add(new_item_entry)
                db.commit()
                return {"description": "Успешный ответ."}

    results = {}
    
    return results

@app.post("/api/auth", response_model=schemas.AuthResponse)
async def authenticate(authRequest: schemas.AuthRequest) -> schemas.AuthResponse:
    db = next(get_db())
    user = authenticate_user(db, authRequest.username, authRequest.password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.user_login}, expires_delta=access_token_expires
        )
        return schemas.AuthResponse(token=access_token)

