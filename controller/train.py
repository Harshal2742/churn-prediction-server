from pymongo.database import Database
from fastapi import UploadFile, status, Depends
from fastapi.responses import JSONResponse
import pandas as pd 
import numpy as np
import os
from datetime import datetime

from di import database

class TrainModel():

  def __init__(self,db:Database =Depends(database.get_db)) -> None:
    self.db = db

  async def train_model():
    pass
  
  async def data_preprocessing(self,csv_file):
    pass

  async def upload_csv_file(self,dataset:UploadFile):
    if(dataset.content_type != 'text/csv'):
      return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,content={
        'status':'fail',
        'message':'Dataset should be CSV file!'
      })
    

    dir = 'dataset'
    os.makedirs(dir,exist_ok=True)
    
    
    for old_file in os.listdir(dir):
      os.unlink(f'{dir}/{old_file}')


    file_name = dataset.filename

    file_content = dataset.file.read()
    with open(f'{dir}/{file_name}',mode='wb') as file:
      file.write(file_content)

    dataset_collection = self.db.get_collection('dataset')

    doc_count: int = await dataset_collection.count_documents({})
    if doc_count > 0:
      await dataset_collection.delete_many({})

    print('Document count : ',doc_count)

    await dataset_collection.insert_one({
      'file_name':file_name,
      'upload_date_time':datetime.utcnow()
    })

    return JSONResponse(status_code=status.HTTP_200_OK,content={
      'status':'success',
      'message':'File uploaded successfully!'
    })
    