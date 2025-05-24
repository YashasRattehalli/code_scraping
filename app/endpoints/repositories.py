from fastapi import APIRouter, Query
from typing import List, Optional

from app.schemas.repository import RepositoryDiscoveryResponse
from app.services.github_service import GitHubService

router = APIRouter()


@router.get("/discover", response_model=RepositoryDiscoveryResponse)
async def discover_repositories(
    min_stars: int = Query(default=0, ge=0, description="Minimum number of stars"),
    min_forks: int = Query(default=0, ge=0, description="Minimum number of forks"),
    languages: Optional[List[str]] = Query(default=None, description="Programming languages to filter by"),
    top_k: int = Query(default=10, ge=1, le=100, description="Maximum number of repositories to return"),
    sort: str = Query(default="stars", pattern="^(stars|forks|updated)$", description="Sort by: stars, forks, or updated")
):
    """
    Discover GitHub repositories based on specified criteria.
    
    - **min_stars**: Minimum number of stars (default: 0)
    - **min_forks**: Minimum number of forks (default: 0)
    - **languages**: List of programming languages to filter by
    - **top_k**: Maximum number of repositories to return (1-100, default: 10)
    - **sort**: Sort repositories by stars, forks, or updated date (default: stars)
    """
    
    return await GitHubService.discover_repositories(
        min_stars=min_stars,
        min_forks=min_forks,
        languages=languages,
        top_k=top_k,
        sort=sort
    ) 