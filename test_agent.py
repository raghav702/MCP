"""Quick test script to verify the agent works."""
import asyncio
from src.main import run_research


async def test_agent():
    """Run a simple test query."""
    test_query = "What are the latest developments in AI agents in 2026?"
    
    print(f"🧪 Testing agent with query: '{test_query}'\n")
    
    try:
        result = await run_research(test_query)
        
        print("\n✅ Test passed!")
        print(f"Report saved to: {result.get('output_path')}")
        print(f"Found {len(result.get('sources', []))} sources")
        print(f"Generated {len(result.get('citations', []))} citations")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent())
