"""MCP tool integrations for web search and filesystem operations."""
import json
import httpx
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient
from bs4 import BeautifulSoup
import html2text
from src.state import Source
from src.config import DEBUG

# Ensure environment variables are loaded
load_dotenv()

# Try to load from Streamlit secrets if available (for deployment)
try:
    import streamlit as st
    if hasattr(st, 'secrets') and 'TAVILY_API_KEY' in st.secrets:
        if not os.getenv('TAVILY_API_KEY'):
            os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_API_KEY']
except:
    pass


class MCPWebSearch:
    """Web search using Tavily API."""
    
    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.use_tavily = bool(self.tavily_api_key)
        
        if self.use_tavily:
            self.client = TavilyClient(api_key=self.tavily_api_key)
        
        if DEBUG:
            if self.use_tavily:
                print("[SEARCH] Using Tavily Search API")
            else:
                print("[SEARCH] Using mock mode - set TAVILY_API_KEY for real search")
    
    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        """Execute web search and return sources."""
        
        if not self.use_tavily:
            return self._mock_search(query, max_results)
        
        try:
            # Use Tavily search
            response = self.client.search(
                query=query,
                max_results=min(max_results, 10),
                search_depth="basic"
            )
            
            sources = []
            if 'results' in response:
                for i, item in enumerate(response['results']):
                    sources.append(Source(
                        url=item.get('url', ''),
                        title=item.get('title', ''),
                        snippet=item.get('content', '')[:200],  # Tavily returns full content
                        content=item.get('content', ''),  # Store full content
                        relevance_score=item.get('score', 1.0 - (i * 0.05))
                    ))
            
            if DEBUG:
                print(f"[SEARCH] Found {len(sources)} results for: {query}")
            
            return sources
            
        except Exception as e:
            if DEBUG:
                print(f"[Tavily Search Error] {type(e).__name__}: {e}")
            return self._mock_search(query, max_results)
    
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
    """Fetch full article content from web pages."""
    
    def __init__(self):
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = True
        self.h2t.body_width = 0
    
    async def fetch(self, url: str) -> str:
        """Fetch full content from URL."""
        
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse HTML and extract text
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Convert to markdown-like text
                text = self.h2t.handle(str(soup))
                
                # Clean up and limit length
                text = text.strip()
                if len(text) > 3000:
                    text = text[:3000] + "..."
                
                if DEBUG:
                    print(f"[FETCH] Retrieved {len(text)} chars from {url}")
                
                return text
                
        except Exception as e:
            if DEBUG:
                print(f"[Fetch Error] {url}: {e}")
            return self._mock_fetch(url)
    
    def _mock_fetch(self, url: str) -> str:
        """Fallback mock content."""
        return f"""Content from {url}

This article provides detailed information on the topic. Key insights and analysis are included to support comprehensive understanding of the subject matter."""


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
