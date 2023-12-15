from fastapi import APIRouter, status,Request, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/predict',tags=['Predict'])


@router.get('/single-dataset')
def predict_single_value():
  return {'status':'success',
          'message':'predict for single value'}


@router.post('/upload-file')
def predict_multiple_value(dataset:UploadFile):
  
  if(dataset.content_type != 'text/csv'):
    return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,content={
      'status':'fail',
      'message':'Dataset should be CSV file!'
    })