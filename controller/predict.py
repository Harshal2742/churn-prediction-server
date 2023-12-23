
from pymongo.database import Database
from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from di import database
import pandas as pd
from pandas import DataFrame
from schemas.request.predict import PredictSingleValue
from models.train import PreporcessingModel, BestModel
import numpy as np
from numpy import ndarray
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFECV


class PredictController():

  def __init__(self,db:Database =Depends(database.get_db)) -> None:
    self.db = db

  async def predict_single_value(self,value:PredictSingleValue):
    json_data = value.model_dump(by_alias=True,mode='json')
    df = pd.json_normalize(json_data)
    try:
      dataset = await self._data_preprocessing(df)
      result  = await self._predict(dataset)
      
    except Exception as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={
        'status':'fail',
        'message':'Failed to predict value.'
      })
    
    return JSONResponse(status_code=status.HTTP_200_OK,content={
      'status':'success',
      'data':{
        'prediction_result':result.__str__()
      }
    })
  
  async def predict_multiple_value(self,file:UploadFile):

    if(file.content_type != 'text/csv'):
      return JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,content={
        'status':'fail',
        'message':'Dataset should be CSV file!'
      })
    
    try:
      df = pd.read_csv(file.file)
      print(df.dtypes)

      if(len(df.columns) != 20):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={
          'status':'failed',
          'message':'Please upload CSV which contains valid data.'
        })
      
      dataset = await self._data_preprocessing(df)
      result = await self._predict(dataset)
    except HTTPException as e:
      raise e

    except Exception as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={
        'status': 'failed',
        'message':'Failed to predict!. Please try after sometime'
      })

    return JSONResponse(status_code=status.HTTP_200_OK,content={
      'status':'success',
      'data':{
        'prediction_result':result.__str__()
      }
    })
          

  async def _data_preprocessing(self,df:DataFrame):

    # convert the numberic string to number (TotalCharges)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

    X = df.iloc[:,1:]

    # converting the SeniorCitizen from numbric to categorical in for to preprocess
    if(X['SeniorCitizen'].unique().__contains__([0,1])):
      X['SeniorCitizen'] = X['SeniorCitizen'].map({0:'No',1:'Yes'})
  

    # encoding binary feature
    X['gender'] = X['gender'].map({'Male':0,'Female':1})
    

    for col in ['SeniorCitizen','Partner','Dependents','PhoneService','PaperlessBilling']:
      X[col] = X[col].map({'No':0,'Yes':1})

    X = X.values
    collection = self.db.get_collection('preprocessing')
    doc = await collection.find_one({})
    
    preprocessing_obj = PreporcessingModel(**doc)
    ct: ColumnTransformer = pickle.loads(preprocessing_obj.column_transformer)
    sc: StandardScaler = pickle.loads(preprocessing_obj.standart_scalar)
    rfecv:RFECV =  pickle.loads(preprocessing_obj.rfecv)

    X = np.array(ct.transform(X))
    X = sc.transform(X)
    X = rfecv.transform(X)
    return X
  
  async def _predict(self,dataset:ndarray) -> ndarray:
    collection = self.db.get_collection('bestmodel')
    best_model = BestModel(**await collection.find_one({}))
    classifier = pickle.loads(best_model.model)

    return classifier.predict(dataset)