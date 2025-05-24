import httpx
import re
import base64
from typing import List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse
from fastapi import HTTPException

from app.schemas.scraper import (
    ScrapingRequest, ScrapingResponse, CodeSnippet, 
    RepositoryInfo, ScrapingMode
)


class GitHubScraperService:
    """Service for scraping GitHub repositories"""
    
    # Common code file extensions
    CODE_EXTENSIONS = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.jsx': 'React',
        '.tsx': 'TypeScript React', '.java': 'Java', '.cpp': 'C++', '.c': 'C',
        '.cs': 'C#', '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust',
        '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala', '.sh': 'Shell',
        '.sql': 'SQL', '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
        '.vue': 'Vue', '.md': 'Markdown', '.yaml': 'YAML', '.yml': 'YAML',
        '.json': 'JSON', '.xml': 'XML', '.r': 'R', '.m': 'MATLAB',
        '.pl': 'Perl', '.lua': 'Lua', '.dart': 'Dart', '.elm': 'Elm'
    }
    
    @staticmethod
    def _parse_github_url(repo_url: str) -> Tuple[str, str]:
        """Extract owner and repo name from GitHub URL"""
        parsed = urlparse(str(repo_url))
        if parsed.netloc != 'github.com':
            raise HTTPException(status_code=400, detail="Only GitHub URLs are supported")
        
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")
        
        return path_parts[0], path_parts[1]
    
    @staticmethod
    def _detect_language(file_path: str, content: str = "") -> Optional[str]:
        """Detect programming language from file extension"""
        for ext, lang in GitHubScraperService.CODE_EXTENSIONS.items():
            if file_path.lower().endswith(ext):
                return lang
        
        # Additional detection based on content for files without clear extensions
        if content:
            if content.strip().startswith('#!/usr/bin/env python') or 'import ' in content[:100]:
                return 'Python'
            elif content.strip().startswith('#!/bin/bash') or content.strip().startswith('#!/bin/sh'):
                return 'Shell'
        
        return None
    
    @staticmethod
    def _is_code_file(file_path: str) -> bool:
        """Check if file is a code file based on extension"""
        return any(file_path.lower().endswith(ext) for ext in GitHubScraperService.CODE_EXTENSIONS.keys())
    
    @staticmethod
    def _filter_by_time_window(date_str: str, start_year: Optional[int], end_year: Optional[int]) -> bool:
        """Filter items by time window"""
        if not start_year and not end_year:
            return True
        
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            year = date.year
            
            if start_year and year < start_year:
                return False
            if end_year and year > end_year:
                return False
            
            return True
        except:
            return True  # Include if we can't parse the date
    
    @staticmethod
    async def _get_repository_info(owner: str, repo: str) -> RepositoryInfo:
        """Get repository information from GitHub API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "GitHub-Repository-Scraper-Service"
                },
                timeout=30.0
            )
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Repository not found")
            elif response.status_code == 403:
                raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"GitHub API error: {response.text}"
                )
            
            data = response.json()
            return RepositoryInfo(
                name=data["name"],
                full_name=data["full_name"],
                description=data.get("description"),
                language=data.get("language"),
                stars=data["stargazers_count"],
                forks=data["forks_count"],
                created_at=data["created_at"],
                updated_at=data["updated_at"]
            )
    
    @staticmethod
    async def _scrape_files(owner: str, repo: str, top_k: int, start_year: Optional[int], end_year: Optional[int]) -> List[CodeSnippet]:
        """Scrape repository files"""
        snippets = []
        
        async with httpx.AsyncClient() as client:
            # Get repository contents
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/contents",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "GitHub-Repository-Scraper-Service"
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                return snippets
            
            contents = response.json()
            
            # Process files and directories
            for item in contents:
                if len(snippets) >= top_k:
                    break
                
                if item["type"] == "file" and GitHubScraperService._is_code_file(item["name"]):
                    try:
                        # Get file content
                        file_response = await client.get(
                            item["download_url"],
                            timeout=30.0
                        )
                        
                        if file_response.status_code == 200:
                            content = file_response.text
                            
                            # Apply time window filter if specified
                            # For files, we'll use the repository's last update as a proxy
                            if start_year or end_year:
                                # Get file commit info for more accurate dating
                                commits_response = await client.get(
                                    f"https://api.github.com/repos/{owner}/{repo}/commits",
                                    params={"path": item["path"], "per_page": 1},
                                    headers={
                                        "Accept": "application/vnd.github.v3+json",
                                        "User-Agent": "GitHub-Repository-Scraper-Service"
                                    },
                                    timeout=30.0
                                )
                                
                                if commits_response.status_code == 200:
                                    commits = commits_response.json()
                                    if commits and not GitHubScraperService._filter_by_time_window(
                                        commits[0]["commit"]["committer"]["date"], start_year, end_year
                                    ):
                                        continue
                            
                            snippet = CodeSnippet(
                                content=content,
                                file_path=item["path"],
                                language=GitHubScraperService._detect_language(item["name"], content),
                                size_bytes=item["size"],
                                lines_count=len(content.split('\n'))
                            )
                            snippets.append(snippet)
                            
                    except Exception:
                        continue  # Skip files that can't be processed
        
        return snippets
    
    @staticmethod
    async def _scrape_commits(owner: str, repo: str, top_k: int, start_year: Optional[int], end_year: Optional[int]) -> List[CodeSnippet]:
        """Scrape repository commits"""
        snippets = []
        
        # Build time filter for API
        params = {"per_page": min(top_k * 2, 100)}  # Get more to account for filtering
        if start_year:
            params["since"] = f"{start_year}-01-01T00:00:00Z"
        if end_year:
            params["until"] = f"{end_year}-12-31T23:59:59Z"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits",
                params=params,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "GitHub-Repository-Scraper-Service"
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                return snippets
            
            commits = response.json()
            
            for commit in commits:
                if len(snippets) >= top_k:
                    break
                
                try:
                    # Get commit details
                    commit_response = await client.get(
                        commit["url"],
                        headers={
                            "Accept": "application/vnd.github.v3+json",
                            "User-Agent": "GitHub-Repository-Scraper-Service"
                        },
                        timeout=30.0
                    )
                    
                    if commit_response.status_code == 200:
                        commit_data = commit_response.json()
                        
                        # Extract code changes from files
                        for file in commit_data.get("files", []):
                            if len(snippets) >= top_k:
                                break
                            
                            if GitHubScraperService._is_code_file(file["filename"]) and file.get("patch"):
                                snippet = CodeSnippet(
                                    content=file["patch"],
                                    file_path=file["filename"],
                                    language=GitHubScraperService._detect_language(file["filename"]),
                                    size_bytes=len(file["patch"]),
                                    lines_count=len(file["patch"].split('\n')),
                                    commit_sha=commit["sha"],
                                    commit_message=commit["commit"]["message"],
                                    commit_date=commit["commit"]["committer"]["date"],
                                    author=commit["commit"]["author"]["name"]
                                )
                                snippets.append(snippet)
                                
                except Exception:
                    continue
        
        return snippets
    
    @staticmethod
    async def _scrape_pull_requests(owner: str, repo: str, top_k: int, start_year: Optional[int], end_year: Optional[int]) -> List[CodeSnippet]:
        """Scrape repository pull requests"""
        snippets = []
        
        async with httpx.AsyncClient() as client:
            # Get closed pull requests (merged ones contain actual changes)
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/pulls",
                params={"state": "closed", "per_page": min(top_k * 2, 100)},
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "GitHub-Repository-Scraper-Service"
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                return snippets
            
            pulls = response.json()
            
            for pr in pulls:
                if len(snippets) >= top_k:
                    break
                
                # Apply time window filter
                if not GitHubScraperService._filter_by_time_window(pr["created_at"], start_year, end_year):
                    continue
                
                try:
                    # Get PR files
                    files_response = await client.get(
                        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr['number']}/files",
                        headers={
                            "Accept": "application/vnd.github.v3+json",
                            "User-Agent": "GitHub-Repository-Scraper-Service"
                        },
                        timeout=30.0
                    )
                    
                    if files_response.status_code == 200:
                        files = files_response.json()
                        
                        for file in files:
                            if len(snippets) >= top_k:
                                break
                            
                            if GitHubScraperService._is_code_file(file["filename"]) and file.get("patch"):
                                snippet = CodeSnippet(
                                    content=file["patch"],
                                    file_path=file["filename"],
                                    language=GitHubScraperService._detect_language(file["filename"]),
                                    size_bytes=len(file["patch"]),
                                    lines_count=len(file["patch"].split('\n')),
                                    pr_number=pr["number"],
                                    pr_title=pr["title"],
                                    commit_date=pr["created_at"],
                                    author=pr["user"]["login"]
                                )
                                snippets.append(snippet)
                                
                except Exception:
                    continue
        
        return snippets
    
    @staticmethod
    async def scrape_repository(request: ScrapingRequest) -> ScrapingResponse:
        """Main method to scrape a GitHub repository"""
        owner, repo = GitHubScraperService._parse_github_url(str(request.repo_url))
        
        try:
            # Get repository information
            repo_info = await GitHubScraperService._get_repository_info(owner, repo)
            
            # Scrape based on mode
            if request.mode == ScrapingMode.FILES:
                snippets = await GitHubScraperService._scrape_files(
                    owner, repo, request.top_k, request.start_year, request.end_year
                )
            elif request.mode == ScrapingMode.COMMITS:
                snippets = await GitHubScraperService._scrape_commits(
                    owner, repo, request.top_k, request.start_year, request.end_year
                )
            elif request.mode == ScrapingMode.PULL_REQUESTS:
                snippets = await GitHubScraperService._scrape_pull_requests(
                    owner, repo, request.top_k, request.start_year, request.end_year
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid scraping mode")
            
            # Build time window info
            time_window = None
            if request.start_year or request.end_year:
                time_window = {
                    "start_year": request.start_year,
                    "end_year": request.end_year
                }
            
            return ScrapingResponse(
                repository=repo_info,
                mode=request.mode,
                time_window=time_window,
                code_snippets=snippets,
                total_found=len(snippets),  # In a real implementation, this would be the total before limiting
                returned_count=len(snippets)
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