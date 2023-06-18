from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated, Union
from uuid import UUID
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

from pydant import *

app = FastAPI(
    title="FoodStock BackEnd API",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_user(username: str):
    db = next(get_db())
    user = db.query(models.UserInDB).filter(models.UserInDB.username == username).first()
    return user
    
def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    user = get_user(token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.post("/token", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())  # Call the generator function to get the session object
    user_dict = db.query(models.UserInDB).filter(models.UserInDB.username == form_data.username).first()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict.username, "user" :user_dict, "token_type": "bearer"}

    
@app.post("/user", tags=["Authentication"])
def create_user(user : User, password : str, db: Session = Depends(get_db)):
    db_user = models.UserInDB(fname=user.fname, lname=user.lname, dob=user.dob, email=user.email, username=user.username, hashed_password=fake_hash_password(password))
    db.add(db_user)
    db.commit()
    db_user = db.query(models.UserInDB).filter(models.UserInDB.username == user.username).first()
    return db_user

@app.get("/user/me", tags=["Authentication"])
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user

@app.get("/allusers", tags=["Authentication"])
async def read_users(db : Session = Depends(get_db)):
    return db.query(models.UserInDB).all()
    
    
# Path: food.py
@app.post("/stock", tags=["Stock"])
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = models.Stock(
        is_personal=stock.is_personal,
        name=stock.name
    )
    owner = db.query(models.UserInDB).filter(models.UserInDB.id == stock.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner user not found")
    db_stock.owner = owner
    db_stock.can_access = []
    db.add(db_stock)
    db.commit()
    return db_stock

@app.get("/stock/{stock_id}", tags=["Stock"])
def read_stock(stock_id: int, db: Session = Depends(get_db)):
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()

@app.get("/allstock", tags=["Stock"])
def read_all_stock(db: Session = Depends(get_db)):
    return db.query(models.Stock).all()

@app.post("/food", tags=["Food"])
def create_food(food : Food, db: Session = Depends(get_db)):
    db_food = models.Food(name=food.name, description=food.description)
    db.add(db_food)
    db.commit()
    return db_food

@app.get("/food/{food_id}", tags=["Food"])
def read_food(food_id: int, db: Session = Depends(get_db)):
    return db.query(models.Food).filter(models.Food.id == food_id).first()

@app.get("/allfood", tags=["Food"])
def read_all_food(db: Session = Depends(get_db)):
    return db.query(models.Food).all()

@app.post("/categories", tags=["Categories"])
def create_categories(categories : Categories, db: Session = Depends(get_db)):
    db_categories = models.Categories(name=categories.name, description=categories.description)
    db.add(db_categories)
    db.commit()
    return db_categories

@app.get("/categories/{categories_id}", tags=["Categories"])
def read_categories(categories_id: int, db: Session = Depends(get_db)):
    return db.query(models.Categories).filter(models.Categories.id == categories_id).first()

@app.get("/allcategories", tags=["Categories"])
async def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Categories).all()
    return {"categories": categories}

@app.post("/entities", tags=["Entities"])
def create_entities(entities : EntitiesCreate, db: Session = Depends(get_db)):
    db_entity = models.Entities(
        quantity=entities.quantity,
        date_of_consumption=entities.date_of_consumption
    )
    food = db.query(models.Food).filter(models.Food.id == entities.food_id).first()
    stock = db.query(models.Stock).filter(models.Stock.id == entities.stock_id).first()
    category = db.query(models.Categories).filter(models.Categories.id == entities.category_id).first()
    db_entity.food = food
    db_entity.stock = stock
    db_entity.category = category
    db.add(db_entity)
    db.commit()
    return db_entity
    

@app.get("/entities/{entities_id}", tags=["Entities"])
def read_entities(entities_id: int, db: Session = Depends(get_db)):
    return db.query(models.Entities).filter(models.Entities.id == entities_id).first()

@app.get("/allentities", tags=["Entities"])
def read_all_entities(db: Session = Depends(get_db)):
    entities = db.query(models.Entities).all()
    result = []
    
    for entity in entities:
        print(entity.food.id)
    
    return result




