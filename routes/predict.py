from fastapi import APIRouter, status, UploadFile, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/predict',tags=['Predict'])


@router.get('/single-dataset')
def predict_single_value():
  return {'status':'success',
          'message':'predict for single value'}


@router.post('/upload-file')
def predict_multiple_value(dataset:UploadFile):
  
  if(dataset.content_type != 'text/csv'):
    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
  
  return JSONResponse(status_code=status.HTTP_200_OK,content={
    'status':'success',
    'message':'Predicted values'
  })