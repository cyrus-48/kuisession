from fastapi import FastAPI  , Depends , HTTPException  , status 
from sqlalchemy.orm import Session
from  db  import get_db
from models import Todo
from schema import TodoCreate , TodoInDB 
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post('/create/' , response_model=TodoInDB ) 
async def create_todo(todo: TodoCreate , db: Session = Depends(get_db)): 
    #check if the todo already exists
    todo_exists = db.query(Todo).filter(Todo.title == todo.title).first()
    if todo_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f'Todo with title {todo.title} already exists')
    new_todo = Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.get('/todos/' , response_model=List[TodoInDB])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

@app.get('/todos/{id}' , response_model=TodoInDB)
async def get_todo_by_id(id: int , db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'Todo with id {id} not found')
    return todo

@app.put('/todos/update/{id}' , response_model=TodoInDB)
async def update_todo(id: int , todo: TodoCreate , db: Session = Depends(get_db)):
    todo_exists = db.query(Todo).filter(Todo.id == id).first()
    if not todo_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'Todo with id {id} not found')
    db.query(Todo).filter(Todo.id == id).update(todo.dict())
    db.commit()
    updated_todo = db.query(Todo).filter(Todo.id == id).first()
    return updated_todo

@app.patch('/todo/update/status/{id}' ,  response_model=TodoInDB)
async def change_status(id:int , db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'Todo with id {id} not found')
    
    todo.is_completed = True 
    db.commit()
    db.refresh(todo)
    return todo
    
    
    

@app.delete('/todos/destroy/{id}' , response_model=TodoInDB)
async def delete_todo(id: int , db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'Todo with id {id} not found')
    db.delete(todo)
    db.commit()
    return todo





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000 )