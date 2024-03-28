from sqlalchemy import Column , String  , Integer , Boolean
from db import Base 

class Todo(Base):
    __tablename__ = "todos"
    id =  Column(Integer , primary_key=True)
    title = Column(String(50) , unique=True) 
    description = Column(String())
    is_completed = Column(Boolean , default=False)
    
    
    
