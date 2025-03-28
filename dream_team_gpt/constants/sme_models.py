from typing import List, Optional

from pydantic import BaseModel, Field


class SMEConfig(BaseModel):
    """Configuration for a subject matter expert."""
    
    name: str = Field(..., description="Name of the executive")
    expertise: str = Field(..., description="Area of expertise")
    concerns: List[str] = Field(..., description="List of primary concerns")
    personality: str = Field("Professional", description="Personality traits")
    industry_focus: str = Field("Financial services", description="Industry specialization")


class SMETeam(BaseModel):
    """Configuration for a team of subject matter experts."""
    
    members: List[SMEConfig] = Field(..., description="Team members")
    
    @classmethod
    def from_list(cls, data: List[dict]) -> "SMETeam":
        """Create a team from a list of dictionaries."""
        members = [SMEConfig(**item) for item in data]
        return cls(members=members)