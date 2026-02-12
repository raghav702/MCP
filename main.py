"""Main CLI interface for the Research Assistant Agent."""
import asyncio
from src.state import ResearchState
from src.workflow import research_agent
from src.config import DEBUG


def print_banner():
    """Print application banner."""
    print("""
╔════════════════════════════════════════════════╗
║   Research Assistant Agent - MVP               ║
║   Powered by LangGraph + MCP                   ║
╚════════════════════════════════════════════════╝
""")


async def run_research(query: str) -> ResearchState:
    """
    Execute research workflow for a given query.
    
    Args:
        query: The research question to investigate
        
    Returns:
        Final ResearchState with results
    """
    # Initialize state
    initial_state = ResearchState(
        query=query,
        current_step="init"
    )
    
    # Run the workflow
    if DEBUG:
        print(f"\n🚀 Starting research workflow for: '{query}'\n")
        print("=" * 60)
    
    final_state = await research_agent.ainvoke(initial_state)
    
    if DEBUG:
        print("=" * 60)
        print(f"\n✅ Research complete! Report saved to: {final_state.get('output_path')}")
    
    return final_state


def main():
    """Main CLI entry point."""
    print_banner()
    
    print("Welcome to the Research Assistant Agent!")
    print("This AI agent will research any topic and generate a comprehensive report.\n")
    
    # Get user input
    query = input("Enter your research query: ").strip()
    
    if not query:
        print("❌ No query provided. Exiting.")
        return
    
    print(f"\n📚 Researching: {query}")
    print("This may take 30-60 seconds...\n")
    
    # Run research
    try:
        final_state = asyncio.run(run_research(query))
        
        # Display results
        print("\n" + "=" * 60)
        print("RESEARCH REPORT")
        print("=" * 60 + "\n")
        
        report = final_state.get('synthesized_report', 'No report generated')
        print(report)
        
        print("\n" + "=" * 60)
        print("SOURCES")
        print("=" * 60 + "\n")
        
        for citation in final_state.get('citations', []):
            print(f"  {citation}")
        
        print(f"\n📄 Full report saved to: {final_state.get('output_path')}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Research cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during research: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
