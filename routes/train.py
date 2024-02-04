import re
from fastapi import APIRouter, status, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from controller.train import TrainModel
from models.train import BestModel
from schemas.response.train import GetAllModelsInformationResponse

router = APIRouter(prefix='/train',tags=['Train'])

@router.get('/train-model')
async def train_model(train_controller:TrainModel = Depends(TrainModel)):
  return await train_controller.train_model()

@router.post('/upload-dataset')
async def upload_dataset(dataset:UploadFile, train_controller:TrainModel = Depends(TrainModel)):
  response: JSONResponse = await train_controller.upload_csv_file(dataset)
  return response

@router.get('/get-all-models', response_model=GetAllModelsInformationResponse)
async def get_all_models(train_controller:TrainModel = Depends(TrainModel)):
  response: GetAllModelsInformationResponse = await train_controller.get_all_models()
  return response;