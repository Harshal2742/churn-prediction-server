from fastapi import APIRouter, Depends
from schemas.request.user import CreateUser, Login
from controller.auth import AuthContoller
from pymongo.database import Database

router = APIRouter(tags=['Auth'])

@router.post('/create-user')
async def create_user(data:CreateUser, auth_controller:AuthContoller = Depends(AuthContoller)):
  response = await auth_controller.create_new_user(data)
  return response


@router.post('/auth')
async def login(data:Login, auth_controller:AuthContoller = Depends(AuthContoller)):
  response = await auth_controller.login_user(data)
  return response