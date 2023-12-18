from pymongo.database import Database
from fastapi import UploadFile, status, Depends
from fastapi.responses import JSONResponse
from models.train import DatasetModel
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import  ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
import pandas as pd 
import numpy as np
import os
from datetime import datetime

from di import database

class TrainModel():

  def __init__(self,db:Database =Depends(database.get_db)) -> None:
    self.db = db

  async def train_model(self):
    X_train, X_test, y_train, y_test = await self.data_preprocessing()

    return JSONResponse(status_code=status.HTTP_200_OK,content={
      'status':'success',
      'message':'Trained model successfully'
    })

  
  async def data_preprocessing(self):
    
    dataset_info = DatasetModel(**await self.db.get_collection('dataset').find_one({}))
    df = pd.read_csv(f'dataset/{dataset_info.file_name}')
    
    df['TotalCharges'].replace(" ",np.nan,inplace=True)
    df.dropna(subset=['TotalCharges'], inplace=True)

    # convert the numberic string to number (TotalCharges)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

    # converting the SeniorCitizen from numbric to categorical in for to preprocess
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0:'Yes',1:'No'})

    X = df.iloc[:,1:-1]
    y = df.iloc[:,-1]

    # encoding binary feature
    X['gender'] = X['gender'].map({'Male':0,'Female':1})

    y = y.map({'No':0,'Yes':1})

    for col in ['SeniorCitizen','Partner','Dependents','PhoneService','PaperlessBilling']:
      X[col] = X[col].map({'No':0,'Yes':1})

    y = y.values

    one_hot_encode_idx = []

    for idx, col in enumerate(X.columns):
        unique_count = len(df[col].unique())
        
        if unique_count == 3 or unique_count == 4:
            one_hot_encode_idx.append(idx)

    X = X.values

    # encoding the categorical data
    ct = ColumnTransformer(transformers=[('one_hot_encoder',OneHotEncoder(),one_hot_encode_idx)], remainder='passthrough')
    X = np.array(ct.fit_transform(X))

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30,random_state=50)
    estimator = LogisticRegression()
    rfecv = RFECV(estimator, cv=StratifiedKFold(10, random_state=50, shuffle=True), scoring="accuracy")
    rfecv.fit(X_train, y_train)

    X_train_rfe = rfecv.transform(X_train)
    X_test_rfe = rfecv.transform(X_test)

    return X_train_rfe, X_test_rfe, y_train, y_test
    

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
    