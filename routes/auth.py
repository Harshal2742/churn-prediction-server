from fastapi import APIRouter, Depends
from controller import auth
from schemas.request.user import CreateUser, Login
from controller.auth import AuthContoller
from pymongo.database import Database
import controller.auth

from schemas.response.user import CreateUserResponse, GetCurrentUserResponse

router = APIRouter(tags=['Auth'])

@router.post('/create-user',response_model=CreateUserResponse)
async def create_user(data:CreateUser, auth_controller:AuthContoller = Depends(AuthContoller)):
  response = await auth_controller.create_new_user(data)
  return response


@router.post('/auth', response_model=CreateUserResponse)
async def login(data:Login, auth_controller:AuthContoller = Depends(AuthContoller)):
  response = await auth_controller.login_user(data)
  return response

@router.get('/current-user',response_model=GetCurrentUserResponse)
async def get_current_user(token:str = Depends(auth.oauth2_scheme),auth_controller:AuthContoller = Depends(AuthContoller)):
  pass