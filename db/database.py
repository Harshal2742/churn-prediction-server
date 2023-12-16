from motor import motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv('.env',override=False)

db_url = os.getenv('MONGODB_URL')
password = os.getenv('DB_PASSWORD')
username = os.getenv('DB_USERNAME')


url = db_url.replace('<password>',password).replace('<username>',username)


try:
  client = motor_asyncio.AsyncIOMotorClient(url)
  print('Connected successfully')
except Exception as e:
  print(e)
  raise

def get_db():
  return client.get_database('churnprediction')