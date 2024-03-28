from pydantic import BaseModel
from typing import List, Optional

class  Todo(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    
class TodoCreate(Todo):
    pass

class TodoInDB(Todo):
    id: int
    class Config:
        orm_mode = True
        