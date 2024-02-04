import string
from fastapi import APIRouter, UploadFile, Depends
from schemas.request.predict import PredictSingleValue
from controller.predict import PredictController

from schemas.response.Predict import PredictMultipleValueResult, PredictSingleValueResult

router = APIRouter(prefix='/predict',tags=['Predict'])


@router.post('/single-dataset', response_model=PredictSingleValueResult )
async def predict_single_value(single_value:PredictSingleValue,selected_model_id:str,predict_controller:PredictController = Depends(PredictController)):
  response = await predict_controller.predict_single_value(single_value,selected_model_id)
  return response


@router.post('/upload-file', response_model=PredictMultipleValueResult)
async def predict_multiple_value(dataset:UploadFile,selected_model_id:str,predict_controller:PredictController = Depends(PredictController)):
  response = await predict_controller.predict_multiple_value(dataset,selected_model_id)
  return response