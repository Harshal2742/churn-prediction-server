from fastapi import APIRouter, status, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from controller.train import TrainModel

router = APIRouter(prefix='/train',tags=['Train'])

@router.get('/train-model')
def train_model():
  return JSONResponse(status_code=status.HTTP_200_OK,content={
    'status':'success',
    'message':'Training the model'
  })


@router.post('/upload-dataset')
async def upload_dataset(dataset:UploadFile, train_controller:TrainModel = Depends(TrainModel)):
  response: JSONResponse = await train_controller.upload_csv_file(dataset)
  return response