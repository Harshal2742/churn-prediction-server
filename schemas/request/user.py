from pydantic import BaseModel,EmailStr, Field

class CreateUser(BaseModel):
  email:EmailStr
  password:str
  confirm_password:str = Field(...)

class Login(BaseModel):
  email: EmailStr
  password: str