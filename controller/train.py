from pymongo.database import Database
from FastAPI import UploadFile
import pandas as pd 
import numpy as np

from sklearn.ensemble import RandomForestClassifier

class TrainModel():

  def __init__(self,db:Database) -> None:
    self.db = db

  # async def train_model():
  
  async def data_preprocessing(self,csv_file):
    pass

  async def upload_csv_file(self,csv_file:UploadFile):
    pass