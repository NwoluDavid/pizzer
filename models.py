from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import List
import json
from sqlalchemy import TypeDecorator, Unicode


class UserCreate(SQLModel):
    username :str
    email : str = Field(index=True)
    password : str
    phone_number: int
    is_active : bool | None = Field(default=False)
    is_staff : bool | None = Field(default= False)
   
class User(UserCreate, table= True):
    id: int | None = Field(default = None, primary_key=True)
    choice: List["Choice"] = Relationship(back_populates="user")
  

class Orderstatus(str, Enum):
    pending= "pending"
    in_transit = "in-transit"
    delivered = "delivered"
 
class Flavour(str , Enum):
    pass
    
class Pizzasize(str ,Enum):
    small ="small"
    medium ="medium"
    large = "large"
    extra_large ="extra-large"
     
class Booking(SQLModel):
    qauntity: int
    order_status: Orderstatus =Field(default ="pending")
    pizza_size: Pizzasize = Field(default ="small")
    flavour: str
   
    
    
class Choice(Booking , table =True):
    id : int| None = Field(default= None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="choice")
    