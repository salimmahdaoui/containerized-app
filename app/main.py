from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, field_validator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.DB.database import get_db
from app.DB.models import Task
from app.DB.schemas import TaskCreate, TaskResponse
from sqlalchemy import select

# Create the FastAPI application
app = FastAPI(
    title="Task Manager API",
    version="0.1.0"
)


# Pydantic model: validates incoming task data
class TaskCreate(BaseModel):
    title: str
    description: str

# PUT/PATCH  Pydantic model: validates complete task updates
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title", "description")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.get("/api/v1/info")
def second_endpoint():
    return {
    "application": "Task Manager API",
    "version": "0.1.0",
    "description": "A containerized task management service" 
            }

@app.post(
    "/api/v1/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    new_task = Task(
        title=task.title,
        description=task.description
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except Exception:
        db.rollback()
        raise

# Get all tasks
@app.get(
    "/api/v1/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(db: Session = Depends(get_db)):

    statement = select(Task)
    result = db.scalars(statement).all()

    return result

# Get a task by ID
@app.get(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(task_id: int, db: Session = Depends(get_db)):

    statement = select(Task).where(Task.id == task_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task



# Delete a task by ID
@app.delete("/api/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):

    statement = select(Task).where(Task.id == task_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    try:
        db.delete(task)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return Response(status_code=204)

# Replace a task completely
@app.put(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    try:
        task.title = updated_task.title
        task.description = updated_task.description

        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise
# Update selected fields of a task
@app.patch(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse
)
def patch_task(
    task_id: int,
    updated_fields: TaskUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    try:
        changes = updated_fields.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise


