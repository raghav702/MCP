"""LangGraph workflow for the Research Assistant Agent."""
from langgraph.graph import StateGraph, END
from src.state import ResearchState
from src.agent_nodes import (
    planning_node,
    search_node,
    fetch_node,
    synthesis_node,
    output_node
)


def create_research_workflow():
    """
    Create and compile the research agent workflow.
    
    Workflow:
    START → Planning → Search → Fetch → Synthesis → Output → END
    """
    
    # Initialize graph with ResearchState
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("planning", planning_node)
    workflow.add_node("search", search_node)
    workflow.add_node("fetch", fetch_node)
    workflow.add_node("synthesis", synthesis_node)
    workflow.add_node("output", output_node)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("planning")
    workflow.add_edge("planning", "search")
    workflow.add_edge("search", "fetch")
    workflow.add_edge("fetch", "synthesis")
    workflow.add_edge("synthesis", "output")
    workflow.add_edge("output", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


# Create the compiled workflow (singleton)
research_agent = create_research_workflow()
