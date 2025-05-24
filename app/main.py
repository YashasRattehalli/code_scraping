from fastapi import FastAPI

from app.endpoints import repositories, health, scraper

app = FastAPI(
    title="GitHub Repository Discovery & Scraping Service",
    description="A comprehensive service to discover and scrape GitHub repositories with various criteria and scraping modes",
    version="1.0.0"
)

# Include routers
app.include_router(repositories.router, tags=["repositories"])
app.include_router(scraper.router, tags=["scraper"])
app.include_router(health.router, tags=["health"])


@app.get("/")
async def root():
    return {"message": "GitHub Repository Discovery & Scraping Service"} 