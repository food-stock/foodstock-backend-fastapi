from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class User(Base):
    __tablename__ = "fuser"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    fname = Column(String, index=True)
    lname = Column(String, index=True)
    dob = Column(String, index=True)
    email = Column(String, index=True)
    
class UserInDB(User):
    hashed_password = Column(String, index=True)

class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    entities = relationship("Entities", back_populates="food")
    
class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    is_personal = Column(Boolean, index=True)
    owner_id = Column(Integer, ForeignKey("fuser.id"))
    can_access_id = Column(Integer, ForeignKey("fuser.id"))
    name = Column(String, index=True)
    
    owner = relationship("User", foreign_keys=[owner_id])
    can_access = relationship("User", foreign_keys=[can_access_id])
    
class Entities(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"))
    stock_id = Column(Integer, ForeignKey("stock.id"))
    quantity = Column(Float, index=True)
    date_of_consumption  = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    food = relationship("Food", back_populates="entities")
    stock = relationship("Stock", backref="entities")
    category = relationship("Categories")
