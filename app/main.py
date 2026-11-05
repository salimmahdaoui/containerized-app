from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="Task Manager API",
    version="0.1.0"
)

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
