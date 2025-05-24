# Base models for database entities
# This file is prepared for future database integration

from typing import Optional
from datetime import datetime


class BaseModel:
    """Base model class for database entities"""
    
    def __init__(self):
        self.created_at: Optional[datetime] = None
        self.updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        } 