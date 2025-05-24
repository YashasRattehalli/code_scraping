import httpx
from typing import List, Optional
from fastapi import HTTPException

from app.schemas.repository import RepositoryResponse, RepositoryDiscoveryResponse


class GitHubService:
    """Service for interacting with GitHub API"""
    
    @staticmethod
    async def discover_repositories(
        min_stars: int = 0,
        min_forks: int = 0,
        languages: Optional[List[str]] = None,
        top_k: int = 10,
        sort: str = "stars"
    ) -> RepositoryDiscoveryResponse:
        """
        Discover GitHub repositories based on specified criteria.
        """
        
        # Build search query
        query_parts = []
        
        if min_stars > 0:
            query_parts.append(f"stars:>={min_stars}")
        
        if min_forks > 0:
            query_parts.append(f"forks:>={min_forks}")
        
        if languages:
            language_query = " OR ".join([f"language:{lang}" for lang in languages])
            query_parts.append(f"({language_query})")
        
        # If no specific criteria, search for repositories with at least 1 star
        if not query_parts:
            query_parts.append("stars:>=1")
        
        search_query = " ".join(query_parts)
        
        # GitHub API parameters
        params = {
            "q": search_query,
            "sort": sort,
            "order": "desc",
            "per_page": min(top_k, 100),
            "page": 1
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.github.com/search/repositories",
                    params=params,
                    headers={
                        "Accept": "application/vnd.github.v3+json",
                        "User-Agent": "GitHub-Repository-Discovery-Service"
                    },
                    timeout=120.0
                )
                
                if response.status_code == 403:
                    raise HTTPException(
                        status_code=429,
                        detail="GitHub API rate limit exceeded. Please try again later."
                    )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"GitHub API error: {response.text}"
                    )
                
                data = response.json()
                
                repositories = []
                for repo in data.get("items", []):
                    try:
                        repo_data = RepositoryResponse(
                            name=repo["name"],
                            full_name=repo["full_name"],
                            description=repo.get("description"),
                            html_url=repo["html_url"],
                            stargazers_count=repo["stargazers_count"],
                            forks_count=repo["forks_count"],
                            language=repo.get("language"),
                            created_at=repo["created_at"],
                            updated_at=repo["updated_at"],
                            owner=repo["owner"]
                        )
                        repositories.append(repo_data)
                    except Exception as e:
                        # Skip repositories that don't match our model
                        continue
                
                return RepositoryDiscoveryResponse(
                    repositories=repositories,
                )
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="GitHub API request timed out. Please try again."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to GitHub API: {str(e)}"
            ) 