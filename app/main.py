from fastapi import FastAPI

from app.endpoints import repositories, health

app = FastAPI(
    title="GitHub Repository Discovery Service",
    description="A service to discover GitHub repositories based on various criteria",
    version="1.0.0"
)

# Include routers
app.include_router(repositories.router, tags=["repositories"])
app.include_router(health.router, tags=["health"])


@app.get("/")
async def root():
    return {"message": "GitHub Repository Discovery Service"} 