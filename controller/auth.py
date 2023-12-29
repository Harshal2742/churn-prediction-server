from datetime import datetime, timedelta
import email
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from di.database import get_db
from pymongo.database import Database
from pymongo.results import InsertOneResult
from schemas.request.user import CreateUser
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from models.user import User
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from bson import json_util
from schemas.response.user import CreateUserResponse

ALGORITHM='HS256'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_pwd:str, hashed_pwd:str):
  return pwd_context.verify(plain_pwd, hashed_pwd)


def hashed_pwd(plain_pwd:str):
  return pwd_context.hash(plain_pwd)


def create_access_token(id:str):
  encode_to = {'user_id':id}
  expire_time = datetime.utcnow() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
  encode_to.update({'expire_time':str(expire_time)})
  encoded_jwt = jwt.encode(claims=encode_to,key=SECRET_KEY,algorithm=ALGORITHM)
  return encoded_jwt


async def get_current_user(token:str = Depends(oauth2_scheme), db:Database = Depends(get_db)):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
          'status':'failed',
          'message':'Invalid access token! Please login again'
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
  
  try:
    payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    expire_time = payload.get('expire_time')
    user_id = payload.get('user_id')

    if expire_time == None or user_id == None:
      raise credentials_exception
    
    if expire_time < datetime.utcnow():
      raise credentials_exception
    
    collection = db.get_collection('users')
    user = await collection.find_one({'_id':user_id})

    if not user:
      raise credentials_exception

  except JWTError:
    raise credentials_exception
  
  except Exception:
    raise JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={
      'status':'failed',
      'message':'Something went wrong! Please try after sometime.'
    })
  
  return user


async def get_current_user(token:str = Depends(oauth2_scheme), db:Database = Depends(get_db)):
  pass


async def create_new_user(data:CreateUser, db:Database):
  if data.password != data.confirm_password:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={
      'status':'fail',
      'message':'Confirmed password is not same as password! Please confirm again.'
    })
  
  collection = db.get_collection('users')
  user = User(email=data.email,role='user',password=hashed_pwd(data.password))

  doc_count = await collection.count_documents({'email':user.email})

  if doc_count >= 1:
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={
      'status':'failed',
      'message':'Email already exist',
    })

  doc:InsertOneResult  = await collection.insert_one(user.model_dump())
  access_token = create_access_token(str(doc.inserted_id))
  inserted_doc =await collection.find_one({'_id':doc.inserted_id})
  
  return JSONResponse(status_code=status.HTTP_201_CREATED,content={
    'status':'success',
    'data': CreateUserResponse(**inserted_doc).model_dump_json(),
    'access_token':access_token,
  })