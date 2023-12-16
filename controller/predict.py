
from pymongo.database import Database

class PredictController():

  def __init__(self,db:Database):
    self.db = db

  async def predict_single_value(self):
    pass