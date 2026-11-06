from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, field_validator
from itertools import count

# Create the FastAPI application
app = FastAPI(
    title="Task Manager API",
    version="0.1.0"
)

# Temporary in-memory storage
tasks = []
task_id_counter = count(1)

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

@app.post("/api/v1/tasks", status_code=201)
def create_task(task: TaskCreate):

    new_task = {
    "id": next(task_id_counter),
    **task.model_dump()
    }

    tasks.append(new_task)

    return new_task

# Get all tasks
@app.get("/api/v1/tasks")
def get_tasks():
    return tasks

# Get a task by ID
@app.get("/api/v1/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Delete a task by ID
@app.delete("/api/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# Replace a task completely
@app.put("/api/v1/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:

            tasks[index] = {
                "id": task_id,
                **updated_task.model_dump()
            }

            return tasks[index]

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Update selected fields of a task
@app.patch("/api/v1/tasks/{task_id}")
def patch_task(task_id: int, updated_fields: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:

            task.update(
                updated_fields.model_dump(exclude_unset=True)
            )

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
