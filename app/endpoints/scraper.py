from fastapi import APIRouter, HTTPException
from app.schemas.scraper import ScrapingRequest, ScrapingResponse
from app.services.scraper_service import GitHubScraperService

router = APIRouter()


@router.post("/scrape", response_model=ScrapingResponse)
async def scrape_repository(request: ScrapingRequest):
    """
    Scrape a GitHub repository for code snippets.
    
    **Scraping Modes:**
    - **files**: Scrape source code files from the repository
    - **commits**: Scrape code changes from commit history  
    - **pull_requests**: Scrape code changes from pull requests
    
    **Parameters:**
    - **repo_url**: GitHub repository URL
    - **mode**: Type of scraping (files, commits, or pull_requests)
    - **start_year**: Optional start year for time window filtering
    - **end_year**: Optional end year for time window filtering
    - **top_k**: Maximum number of code samples to return (1-100, default: 10)
    """
    
    try:
        return await GitHubScraperService.scrape_repository(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during scraping: {str(e)}"
        ) 