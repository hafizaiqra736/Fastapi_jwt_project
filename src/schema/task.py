from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[datetime]

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config :
        from_attributes = True