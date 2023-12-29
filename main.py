from fastapi import FastAPI,Depends
from routes import predict, train, auth
from controller.auth import oauth2_scheme


app = FastAPI()

app.include_router(predict.router,dependencies=[Depends(oauth2_scheme)])
app.include_router(train.router,dependencies=[Depends(oauth2_scheme)])
app.include_router(auth.router)
@app.get('/')
def main():
  return {'status':'success','message':'Hello World'}