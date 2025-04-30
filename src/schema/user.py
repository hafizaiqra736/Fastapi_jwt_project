from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    is_active: bool

    class Config:
      from_attributes = True
    