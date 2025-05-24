from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class RepositoryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stars: int = Field(alias="stargazers_count", serialization_alias="stars")
    forks: int = Field(alias="forks_count", serialization_alias="forks")
    language: Optional[str]
    created_at: str
    updated_at: str
    owner: dict


class RepositoryDiscoveryResponse(BaseModel):
    repositories: List[RepositoryResponse]
