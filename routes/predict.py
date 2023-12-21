from fastapi import APIRouter, status, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from schemas.request.predict import PredictSingleValue

router = APIRouter(prefix='/predict',tags=['Predict'])


@router.post('/single-dataset')
def predict_single_value(single_value:PredictSingleValue):
  print(single_value.model_dump_json(by_alias=True))
  return {'status':'success',
          'message':'Hello'}


@router.post('/upload-file')
def predict_multiple_value(dataset:UploadFile):
  
  if(dataset.content_type != 'text/csv'):
    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
  
  return JSONResponse(status_code=status.HTTP_200_OK,content={
    'status':'success',
    'message':'Predicted values'
  })