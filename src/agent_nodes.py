"""Agent nodes for the LangGraph workflow."""
from typing import Dict, Any
from src.state import ResearchState, Source
from src.llm import get_llm, create_prompt
from src.mcp_tools import web_search, web_fetch, filesystem
from src.config import MAX_SEARCH_RESULTS, MAX_SOURCES_TO_FETCH, DEBUG


async def planning_node(state: ResearchState) -> Dict[str, Any]:
    """
    Planning phase: Break down the research query into subtopics and search strategy.
    """
    if DEBUG:
        print(f"\n[PLANNING] Analyzing query: '{state.query}'")
    
    llm = get_llm(temperature=0.3)
    
    planning_prompt = create_prompt(
        """You are a research planning assistant. Given a research query, break it down into 3-5 specific subtopics that should be investigated.

Research Query: {query}

Output your response in this exact format:
SUBTOPICS:
1. [First subtopic]
2. [Second subtopic]
3. [Third subtopic]

SEARCH STRATEGY:
[Brief description of how to approach this research]""",
        query=state.query
    )
    
    response = await llm.ainvoke(planning_prompt)
    response_text = response.content
    
    # Parse subtopics
    subtopics = []
    search_strategy = ""
    
    lines = response_text.split('\n')
    in_subtopics = False
    in_strategy = False
    
    for line in lines:
        line = line.strip()
        if 'SUBTOPICS:' in line:
            in_subtopics = True
            in_strategy = False
            continue
        elif 'SEARCH STRATEGY:' in line:
            in_subtopics = False
            in_strategy = True
            continue
        
        if in_subtopics and line:
            # Remove numbering
            cleaned = line.lstrip('0123456789.-) ')
            if cleaned:
                subtopics.append(cleaned)
        elif in_strategy and line:
            search_strategy += line + " "
    
    if DEBUG:
        print(f"[PLANNING] Identified {len(subtopics)} subtopics")
        for i, topic in enumerate(subtopics, 1):
            print(f"  {i}. {topic}")
    
    return {
        "subtopics": subtopics,
        "search_strategy": search_strategy.strip(),
        "current_step": "planning_complete"
    }


async def search_node(state: ResearchState) -> Dict[str, Any]:
    """
    Search phase: Execute searches for each subtopic and collect sources.
    """
    if DEBUG:
        print(f"\n[SEARCHING] Executing searches for {len(state.subtopics)} subtopics")
    
    all_sources = []
    search_queries = []
    
    # Generate search queries from subtopics
    for subtopic in state.subtopics:
        query = f"{state.query} {subtopic}"
        search_queries.append(query)
        
        if DEBUG:
            print(f"  Searching: {query}")
        
        # Execute search
        sources = await web_search.search(query, max_results=MAX_SEARCH_RESULTS // len(state.subtopics))
        all_sources.extend(sources)
    
    # Sort by relevance and deduplicate
    seen_urls = set()
    unique_sources = []
    for source in sorted(all_sources, key=lambda x: x.relevance_score, reverse=True):
        if source.url not in seen_urls:
            seen_urls.add(source.url)
            unique_sources.append(source)
    
    if DEBUG:
        print(f"[SEARCHING] Found {len(unique_sources)} unique sources")
    
    return {
        "search_queries": search_queries,
        "sources": unique_sources,
        "current_step": "search_complete"
    }


async def fetch_node(state: ResearchState) -> Dict[str, Any]:
    """
    Fetch phase: Get full content from top sources.
    """
    if DEBUG:
        print(f"\n[FETCHING] Reading top {MAX_SOURCES_TO_FETCH} sources")
    
    fetched_content = []
    
    # Fetch top sources
    for i, source in enumerate(state.sources[:MAX_SOURCES_TO_FETCH]):
        if DEBUG:
            print(f"  {i+1}. {source.title}")
        
        content = await web_fetch.fetch(source.url)
        source.content = content
        
        fetched_content.append({
            "url": source.url,
            "title": source.title,
            "content": content
        })
    
    return {
        "fetched_content": fetched_content,
        "sources": state.sources,  # Updated sources with content
        "current_step": "fetch_complete"
    }


async def synthesis_node(state: ResearchState) -> Dict[str, Any]:
    """
    Synthesis phase: Generate comprehensive report with citations.
    """
    if DEBUG:
        print(f"\n[SYNTHESIZING] Generating research report")
    
    llm = get_llm(temperature=0.7)
    
    # Prepare source summaries for context
    source_context = ""
    for i, source in enumerate(state.sources[:MAX_SOURCES_TO_FETCH], 1):
        source_context += f"\n[Source {i}] {source.title}\nURL: {source.url}\n"
        if source.content:
            source_context += f"Content: {source.content[:500]}...\n"
        else:
            source_context += f"Snippet: {source.snippet}\n"
        source_context += "\n"
    
    synthesis_prompt = create_prompt(
        """You are a research analyst. Create a comprehensive research report based on the following information.

Original Query: {query}

Subtopics Investigated:
{subtopics}

Available Sources:
{sources}

Generate a well-structured research report with:
1. Executive Summary
2. Detailed Findings (organized by subtopic)
3. Key Insights
4. Conclusion

Use [Source X] notation to cite sources throughout the report. Be factual and analytical.""",
        query=state.query,
        subtopics="\n".join(f"- {t}" for t in state.subtopics),
        sources=source_context
    )
    
    response = await llm.ainvoke(synthesis_prompt)
    synthesized_report = response.content
    
    # Generate citations
    citations = [
        f"[{i}] {source.title} - {source.url}"
        for i, source in enumerate(state.sources[:MAX_SOURCES_TO_FETCH], 1)
    ]
    
    if DEBUG:
        print(f"[SYNTHESIZING] Report generated ({len(synthesized_report)} chars)")
    
    return {
        "synthesized_report": synthesized_report,
        "citations": citations,
        "current_step": "synthesis_complete"
    }


async def output_node(state: ResearchState) -> Dict[str, Any]:
    """
    Output phase: Save report to filesystem.
    """
    if DEBUG:
        print(f"\n[OUTPUT] Saving report")
    
    # Create full report with citations
    full_report = f"""# Research Report: {state.query}

{state.synthesized_report}

---

## References

{chr(10).join(state.citations)}

---
Generated by Research Assistant Agent
"""
    
    # Generate filename
    filename = state.query.lower().replace(' ', '_')[:50] + '.md'
    
    # Save to filesystem
    output_path = filesystem.save_report(full_report, filename)
    
    if DEBUG:
        print(f"[OUTPUT] Report saved to: {output_path}")
    
    return {
        "output_path": output_path,
        "current_step": "complete"
    }
