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
