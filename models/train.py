from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class DatasetModel(BaseModel):
  """
   Model for dataset information
  """
  id: Optional[PyObjectId]= Field(alias='_id', default=None)
  file_name: str = Field(...)
  upload_date_time: datetime = Field(...)
