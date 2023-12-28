from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

# async def create_user(email:)

async def get_current_user(token:str = Depends(oauth2_scheme)):
  pass