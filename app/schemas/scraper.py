from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from enum import Enum


class ScrapingMode(str, Enum):
    """Enum for different scraping modes"""
    FILES = "files"
    COMMITS = "commits"
    PULL_REQUESTS = "pull_requests"


class ScrapingRequest(BaseModel):
    """Request model for GitHub repo scraping"""
    repo_url: HttpUrl = Field(..., description="GitHub repository URL")
    mode: ScrapingMode = Field(..., description="Type of scraping: files, commits, or pull_requests")
    start_year: Optional[int] = Field(None, description="Start year for time window filter")
    end_year: Optional[int] = Field(None, description="End year for time window filter")
    top_k: int = Field(default=10, description="Maximum number of code samples to return")


class CodeSnippet(BaseModel):
    """Model for individual code snippets"""
    content: str = Field(..., description="The actual code content")
    file_path: str = Field(..., description="Path to the file in the repository")
    language: Optional[str] = Field(None, description="Programming language detected")
    size_bytes: int = Field(..., description="Size of the code snippet in bytes")
    lines_count: int = Field(..., description="Number of lines in the code snippet")
    
    # For commits/PR mode
    commit_sha: Optional[str] = Field(None, description="Commit SHA (for commit/PR mode)")
    commit_message: Optional[str] = Field(None, description="Commit message (for commit/PR mode)")
    commit_date: Optional[str] = Field(None, description="Commit date (for commit/PR mode)")
    author: Optional[str] = Field(None, description="Author name (for commit/PR mode)")
    
    # For PR mode
    pr_number: Optional[int] = Field(None, description="Pull request number (for PR mode)")
    pr_title: Optional[str] = Field(None, description="Pull request title (for PR mode)")


class RepositoryInfo(BaseModel):
    """Repository metadata"""
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    description: Optional[str] = Field(None, description="Repository description")
    language: Optional[str] = Field(None, description="Primary programming language")
    stars: int = Field(..., description="Number of stars")
    forks: int = Field(..., description="Number of forks")
    created_at: str = Field(..., description="Repository creation date")
    updated_at: str = Field(..., description="Repository last update date")


class ScrapingResponse(BaseModel):
    """Response model for GitHub repo scraping"""
    repository: RepositoryInfo = Field(..., description="Repository information")
    mode: ScrapingMode = Field(..., description="Scraping mode used")
    time_window: Optional[dict] = Field(None, description="Time window filter applied")
    code_snippets: List[CodeSnippet] = Field(..., description="List of scraped code snippets")
    total_found: int = Field(..., description="Total number of items found before top_k limit")
    returned_count: int = Field(..., description="Number of items returned (limited by top_k)") 