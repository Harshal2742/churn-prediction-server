from fastapi import APIRouter, status, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.request.predict import PredictSingleValue
from controller.predict import PredictController
import pandas as pd

from schemas.response.Predict import PredictMultipleValueResult, PredictSingleValueResult

router = APIRouter(prefix='/predict',tags=['Predict'])


@router.post('/single-dataset', response_model=PredictSingleValueResult )
async def predict_single_value(single_value:PredictSingleValue,predict_controller:PredictController = Depends(PredictController)):
  response = await predict_controller.predict_single_value(single_value)
  return response


@router.post('/upload-file', response_model=PredictMultipleValueResult)
async def predict_multiple_value(dataset:UploadFile,predict_controller:PredictController = Depends(PredictController)):
  response = await predict_controller.predict_multiple_value(dataset)
  return response