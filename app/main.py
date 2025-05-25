from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.endpoints import repositories, health, scraper

# Enhanced FastAPI app configuration for better Swagger UI
app = FastAPI(
    title="GitHub Repository Discovery & Scraping Service",
    description="""
    🚀 **A comprehensive service to discover and scrape GitHub repositories**

    This service provides two main capabilities:

    ## 🔍 Repository Discovery
    - Search repositories by minimum stars and forks
    - Filter by programming languages  
    - Sort by stars, forks, or last updated date
    - Get detailed repository metadata

    ## 🛠️ Code Scraping
    - Extract code snippets from repositories
    - Multiple scraping modes: files, commits, pull requests
    - Time window filtering for commits and PRs
    - Configurable result limits

    ## 📝 Features
    - ✅ Fast and scalable FastAPI backend
    - ✅ Comprehensive error handling
    - ✅ Rate limiting awareness  
    - ✅ Auto-generated API documentation
    - ✅ Async support for better performance

    ## 🔗 Useful Links
    - [GitHub Repository](https://github.com/your-username/repo-discovery-service)
    - [Postman Collection Guide](./static/POSTMAN_GUIDE.md)
    - [Development Guide](./README.md)
    """,
    version="1.0.0",
    contact={
        "name": "GitHub Repository Discovery Service",
        "url": "https://github.com/your-username/repo-discovery-service",
        "email": "your-email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://54.89.84.159:8001",
            "description": "Production server"
        },
        {
            "url": "http://localhost:8001",
            "description": "Development server"
        }
    ],
    # Enhanced OpenAPI configuration
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware to fix Swagger UI "Failed to fetch" errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with enhanced tags and descriptions
app.include_router(
    repositories.router, 
    tags=["🔍 Repository Discovery"],
    prefix="",
)
app.include_router(
    scraper.router, 
    tags=["🛠️ Code Scraping"],
    prefix="",
)
app.include_router(
    health.router, 
    tags=["🏥 Health & Status"],
    prefix="",
)


@app.get(
    "/",
    tags=["🏠 General"],
    summary="Service Information",
    description="Get basic information about the GitHub Repository Discovery & Scraping Service",
    responses={
        200: {
            "description": "Service information",
            "content": {
                "application/json": {
                    "example": {
                        "message": "GitHub Repository Discovery & Scraping Service",
                        "version": "1.0.0",
                        "docs": "/docs",
                        "redoc": "/redoc"
                    }
                }
            }
        }
    }
)
async def root():
    """
    **Welcome to the GitHub Repository Discovery & Scraping Service!**
    
    This endpoint provides basic service information and quick links to documentation.
    
    **Quick Start:**
    - 📖 **Interactive API Docs**: [/docs](/docs)
    - 📚 **Alternative Docs**: [/redoc](/redoc)
    - ❤️ **Health Check**: [/health](/health)
    - 🔍 **Discover Repositories**: [/discover](/discover)
    """
    return {
        "message": "GitHub Repository Discovery & Scraping Service",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


def custom_openapi():
    """Generate custom OpenAPI schema with enhanced documentation"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        servers=app.servers,
    )
    
    # Add custom schema information
    openapi_schema["info"]["x-logo"] = {
        "url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    }
    
    # Enhanced tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "🏠 General",
            "description": "General service information and root endpoints"
        },
        {
            "name": "🔍 Repository Discovery", 
            "description": "Discover GitHub repositories based on various criteria like stars, forks, and programming languages"
        },
        {
            "name": "🛠️ Code Scraping",
            "description": "Scrape code snippets from GitHub repositories using different modes (files, commits, pull requests)"
        },
        {
            "name": "🏥 Health & Status",
            "description": "Health check and service status endpoints"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi 