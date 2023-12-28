from fastapi import FastAPI,Depends
from routes import predict, train
from controller.auth import oauth2_scheme


app = FastAPI(dependencies=[Depends(oauth2_scheme)])

app.include_router(predict.router )
app.include_router(train.router)
@app.get('/')
def main():
  return {'status':'success','message':'Hello World'}