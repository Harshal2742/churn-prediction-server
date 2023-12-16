from fastapi import FastAPI
from routes import predict, train
from db import database
import os

app = FastAPI()



app.include_router(predict.router)
app.include_router(train.router)
@app.get('/')
def main():
  return {'status':'success','message':'Hello World'}