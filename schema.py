from pydantic import BaseModel , Field
from typing import Optional

class SignUpModel(BaseModel):
    username :str
    email : str = Field(index=True)
    password : str
    phone_number: int
    is_active : Optional[bool ]
    is_staff : Optional[bool ]
    
    class config:
        orm_mode =True
        schema_extra ={
            "username": "john Doe",
            "email":"user@gmail.com",
            "password" : "password",
            "is_staff": False,
            "is_active":True  
        }
        
class Settings(BaseModel):
    authjwt_secret_key: str= 'b47e14b326edca116bc5740b82031f57f743565e4afb75d2888b3c9958625bf2'
    
class LoginModel(BaseModel):
    username:str
    password: str
    

        
