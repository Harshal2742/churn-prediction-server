from fastapi import APIRouter, Depends
from di.database import get_db
from schemas.request.user import CreateUser
from controller.auth import create_new_user
from pymongo.database import Database

router = APIRouter(tags=['Auth'])

@router.post('/create-user')
async def create_user(data:CreateUser,db:Database = Depends(get_db)):
  response = await create_new_user(data,db)
  return response