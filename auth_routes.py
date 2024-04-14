from fastapi import APIRouter , Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import UserCreate , User
from deps import get_db
from typing import Annotated
from sqlmodel import Session
from schema import SignUpModel,LoginModel
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router=APIRouter(prefix= "/auth" , tags = ["auth"])



@auth_router.get("/")
async def hello():
    return {"message": "Hello World!"}


@auth_router.post("/signup", status_code=201)
async def signup(
    user: SignUpModel, 
    db: Annotated[Session,  Depends(get_db)]
):
    db_email =db.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code =status.HTTP_400_BAD_REQUEST, 
        detail ="user this email already exists")
    
    db_username =db.query(User).filter(User.username == user.email).first()

    if db_username is not None:
        return HTTPException(status_code =status.HTTP_400_BAD_REQUEST, 
        detail ="user this email already exists")
    
    
    
    new_user = User( 
        username= user.username,       
        email=user.email,
        phone_number=user.phone_number,
        password=generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return JSONResponse(status_code=201, content = new_user.model_dump())
    return new_user
    
@auth_router.post("/login" , status_code =200)   
async def login(
user:LoginModel,
db: Annotated[Session,  Depends(get_db)],
Authorize:AuthJWT =Depends()

):
    db_user =db.query(user).filter(User.username == user.username).first()
    
    if db_user and check_password_hash(db_user.password,user.password):
        access_token =Authorize.create_access_token(subject =db_user.username)
        refresh_token =Authorize.create_refresh_token(subject =db_user.username)
        
        response = {
            "access":access_token,
            "refresh":refresh_token
        }
        
        return jsonable_encoder(response)
    
    raise HTTPException(status_code =status.HTTP_400_BAD_REQUEST,
                        detail = "invalid username or password"
    )

