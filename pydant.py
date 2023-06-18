from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    fname: str
    lname: str
    dob: str
    email: str

class User(UserBase):
    id: int

class UserInDB(User):
    hashed_password: str

class FoodBase(BaseModel):
    name: str
    description: str

class Food(FoodBase):
    id: int
    entities: List["Entities"] = []

class Categories(BaseModel):
    id: int
    name: str
    description: str

class Stock(BaseModel):
    id : int
    is_personal: bool
    owner_id: int
    can_access_id: int
    name: str

class EntitiesBase(BaseModel):
    quantity: float
    date_of_consumption: str
    food_id: int
    stock_id: int
    category_id: int

class Entities(EntitiesBase):
    id: int
    food: Food
    stock: Stock
    category: Categories


class StockCreate(BaseModel):
    is_personal: bool
    owner_id: int
    name: str
    
class EntitiesCreate(BaseModel):
    food_id: int
    stock_id: int
    category_id: int
    quantity: float
    date_of_consumption: str