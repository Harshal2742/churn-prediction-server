from fastapi import APIRouter, status,Request, UploadFile
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/train',tags=['Train'])

@router.get('/train-model')
def train_model():
  return JSONResponse(status_code=status.HTTP_200_OK,content={
    'status':'success',
    'message':'Training the model'
  })


@router.post('/upload-dataset')
def upload_dataset(dataset:UploadFile):

  if(dataset.content_type != 'text/csv'):
    return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,content={
      'status':'fail',
      'message':'Dataset should be CSV file!'
    })
  
  return {
    'status':'success',
    'message':'File uploaded successfully'
  }