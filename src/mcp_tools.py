"""MCP tool integrations for web search and filesystem operations."""
import json
import httpx
from typing import List, Dict, Any
from src.state import Source
from src.config import DEBUG


class MCPWebSearch:
    """Simple web search via MCP (mock for MVP - replace with actual MCP later)."""
    
    def __init__(self):
        self.mock_mode = True  # Set to False when MCP server is running
    
    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        """Execute web search and return sources."""
        
        if self.mock_mode:
            # Mock search results for MVP testing
            return self._mock_search(query, max_results)
        
        # Actual MCP call (implement when MCP server is ready)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:3000/search",
                    json={"query": query, "max_results": max_results}
                )
                results = response.json()
                return [Source(**r) for r in results]
        except Exception as e:
            if DEBUG:
                print(f"[MCP Search Error] {e}")
            return []
    
    def _mock_search(self, query: str, max_results: int) -> List[Source]:
        """Mock search results for testing."""
        mock_results = [
            Source(
                url=f"https://example.com/article-{i}",
                title=f"Article {i}: {query}",
                snippet=f"This is a relevant article about {query}. It contains important information and insights.",
                relevance_score=0.9 - (i * 0.1)
            )
            for i in range(1, min(max_results + 1, 6))
        ]
        return mock_results


class MCPWebFetch:
    """Fetch full article content via MCP."""
    
    def __init__(self):
        self.mock_mode = True
    
    async def fetch(self, url: str) -> str:
        """Fetch full content from URL."""
        
        if self.mock_mode:
            return self._mock_fetch(url)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:3000/fetch",
                    json={"url": url}
                )
                return response.json().get("content", "")
        except Exception as e:
            if DEBUG:
                print(f"[MCP Fetch Error] {e}")
            return ""
    
    def _mock_fetch(self, url: str) -> str:
        """Mock article content."""
        return f"""# Full Article Content from {url}

This is the full content of the article. In a production environment, this would be the actual scraped content from the web page.

## Key Points:
- Important insight 1
- Important insight 2
- Important insight 3

The article provides detailed analysis and data supporting the research query."""


class MCPFilesystem:
    """Filesystem operations via MCP."""
    
    @staticmethod
    def save_report(content: str, filename: str, output_dir: str = "reports") -> str:
        """Save report to filesystem."""
        from pathlib import Path
        
        output_path = Path(output_dir) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)


# Singleton instances
web_search = MCPWebSearch()
web_fetch = MCPWebFetch()
filesystem = MCPFilesystem()
