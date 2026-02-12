"""State definitions for the Research Assistant Agent."""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Represents a single research source."""
    url: str
    title: str
    snippet: str
    content: Optional[str] = None
    relevance_score: float = 0.0


class ResearchState(BaseModel):
    """State for the research agent workflow."""
    
    # Input
    query: str = Field(description="The original research query")
    
    # Planning phase
    subtopics: List[str] = Field(default_factory=list, description="Decomposed subtopics")
    search_strategy: str = Field(default="", description="Planned search approach")
    
    # Execution phase
    search_queries: List[str] = Field(default_factory=list, description="Generated search queries")
    sources: List[Source] = Field(default_factory=list, description="Found sources")
    fetched_content: List[Dict] = Field(default_factory=list, description="Full article content")
    
    # Synthesis phase
    synthesized_report: str = Field(default="", description="Final research report")
    citations: List[str] = Field(default_factory=list, description="Formatted citations")
    
    # Output phase
    output_path: Optional[str] = Field(default=None, description="Saved report path")
    
    # Metadata
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    current_step: str = Field(default="init", description="Current workflow step")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
