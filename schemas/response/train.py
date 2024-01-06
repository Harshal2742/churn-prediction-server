from pydantic import BaseModel
from pydantic import BaseModel, BeforeValidator, Field
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class CurrentModelInformationResponse(BaseModel):
  id: Optional[PyObjectId]= Field(alias='_id', default=None)
  accurancy: float = Field(...)
  model_name: str = Field(...)
  precision: float = Field(...)
  recall:float = Field(...)
  f_score:float = Field(...)