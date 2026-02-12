"""Streamlit Web UI for Research Assistant Agent."""
import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path
import json
from src.state import ResearchState
from src.workflow import research_agent


# Page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean professional design
st.markdown("""
<style>
    /* Typography */
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    /* Hide branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #3498db;
    }
    
    /* Clean buttons */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    if 'current_report' not in st.session_state:
        st.session_state.current_report = None
    if 'is_researching' not in st.session_state:
        st.session_state.is_researching = False


async def run_research_async(query: str):
    """Run research workflow asynchronously."""
    initial_state = ResearchState(query=query, current_step="init")
    final_state = await research_agent.ainvoke(initial_state)
    return final_state


def run_research(query: str):
    """Run research workflow (sync wrapper)."""
    return asyncio.run(run_research_async(query))


def display_header():
    """Display app header."""
    st.markdown('<h1 class="main-header">Research Assistant Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Research Automation</p>', unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with info and history."""
    with st.sidebar:
        st.markdown("### About")
        st.info("""
        This agent autonomously:
        - Plans research strategy
        - Searches multiple sources
        - Fetches full content
        - Synthesizes findings
        - Saves with citations
        """)
        
        st.markdown("### How It Works")
        st.markdown("""
        1. **Planning** - Breaks query into subtopics
        2. **Search** - Finds relevant sources
        3. **Fetch** - Reads full articles
        4. **Synthesis** - Generates report
        5. **Output** - Ready for download
        """)
        
        st.markdown("### Tech Stack")
        st.markdown("""
        - LangGraph (Orchestration)
        - MCP Protocol (Tools)
        - Gemini (LLM)
        - Tavily (Search)
        - Streamlit (UI)
        """)
        
        st.markdown("---")
        
        # Research History
        if st.session_state.research_history:
            st.markdown("### Research History")
            for i, item in enumerate(reversed(st.session_state.research_history[-5:])):
                with st.expander(f"{item['query'][:50]}..."):
                    st.caption(f"Time: {item['timestamp']}")
                    st.caption(f"Sources: {len(item.get('citations', []))}")
                    if st.button("View Report", key=f"view_{i}"):
                        st.session_state.current_report = item


def display_main_interface():
    """Display main research interface."""
    
    # Query input
    st.markdown("### Start Your Research")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your research query:",
            placeholder="e.g., What are the latest developments in AI agents?",
            label_visibility="collapsed"
        )
    
    with col2:
        research_button = st.button("Research", type="primary", use_container_width=True)
    
    # Example queries
    st.markdown("**Example Queries:**")
    examples = [
        "Compare State Space Models vs Transformers in 2026",
        "Explain the Model Context Protocol and its benefits",
        "What are the best practices for agentic AI in 2026?"
    ]
    
    example_cols = st.columns(3)
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(f"{example[:40]}...", key=f"example_{i}", use_container_width=True):
                st.session_state.example_query = example
                st.rerun()
    
    # Use example query if selected
    if 'example_query' in st.session_state:
        query = st.session_state.example_query
        del st.session_state.example_query
        research_button = True
    
    # Execute research
    if research_button and query:
        execute_research(query)
    
    # Display current report
    if st.session_state.current_report:
        display_report(st.session_state.current_report)


def execute_research(query: str):
    """Execute research workflow with progress display."""
    st.markdown("---")
    st.markdown(f"### Researching: *{query}*")
    
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        ("Planning", "Breaking down query into subtopics...", 20),
        ("Searching", "Finding relevant sources...", 40),
        ("Fetching", "Reading full article content...", 60),
        ("Synthesizing", "Generating comprehensive report...", 80),
        ("Saving", "Finalizing report with citations...", 100)
    ]
    
    # Create placeholder for stages
    stage_container = st.container()
    
    with stage_container:
        stage_cols = st.columns(5)
        stage_indicators = []
        for i, (stage_name, _, _) in enumerate(stages):
            with stage_cols[i]:
                indicator = st.empty()
                stage_indicators.append(indicator)
                indicator.markdown(f"**{stage_name}**", unsafe_allow_html=True)
    
    try:
        # Run research
        with st.spinner("Agent is working..."):
            for i, (stage_name, stage_desc, progress) in enumerate(stages):
                status_text.markdown(f"**{stage_name}**: {stage_desc}")
                progress_bar.progress(progress)
                
                # Highlight current stage
                for j, indicator in enumerate(stage_indicators):
                    if j == i:
                        indicator.markdown(f"✓ **{stages[j][0]}**", unsafe_allow_html=True)
                    elif j < i:
                        indicator.markdown(f"✓ {stages[j][0]}", unsafe_allow_html=True)
                
                # Execute research on last stage
                if i == len(stages) - 1:
                    final_state = run_research(query)
            
            progress_bar.progress(100)
            status_text.markdown("**✓ Research Complete!**")
        
        # Store in history
        research_result = {
            'query': query,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'report': final_state.get('synthesized_report', ''),
            'citations': final_state.get('citations', []),
            'subtopics': final_state.get('subtopics', []),
            'sources': len(final_state.get('sources', [])),
            'output_path': final_state.get('output_path', '')
        }
        
        st.session_state.research_history.append(research_result)
        st.session_state.current_report = research_result
        
        st.success("Research completed successfully!")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        with st.expander("Details"):
            st.exception(e)


def display_report(report: dict):
    """Display research report."""
    st.markdown("---")
    st.markdown("## Research Report")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Sources</div>
        </div>
        """.format(report.get('sources', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Subtopics</div>
        </div>
        """.format(len(report.get('subtopics', []))), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Citations</div>
        </div>
        """.format(len(report.get('citations', []))), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">~30s</div>
            <div class="metric-label">Duration</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Report tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Report", "Subtopics", "Citations", "Export"])
    
    with tab1:
        st.markdown("### Full Research Report")
        st.markdown(report.get('report', 'No report available'))
    
    with tab2:
        st.markdown("### Research Subtopics")
        subtopics = report.get('subtopics', [])
        if subtopics:
            for i, subtopic in enumerate(subtopics, 1):
                st.markdown(f"{i}. {subtopic}")
        else:
            st.info("No subtopics available")
    
    with tab3:
        st.markdown("### Sources & Citations")
        citations = report.get('citations', [])
        if citations:
            for citation in citations:
                st.markdown(f"- {citation}")
        else:
            st.info("No citations available")
    
    with tab4:
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as Markdown
            report_md = f"# {report['query']}\n\n{report.get('report', '')}\n\n## References\n\n"
            report_md += "\n".join(report.get('citations', []))
            
            st.download_button(
                label="Download Markdown",
                data=report_md,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            # Download as JSON
            report_json = json.dumps(report, indent=2)
            st.download_button(
                label="Download JSON",
                data=report_json,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            st.info("Reports are generated on-demand and not saved automatically")
    
    st.markdown("---")
    st.markdown("**Tip:** Use the download buttons to save your research for later")


def display_footer():
    """Display footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #999; padding: 1rem 0; font-size: 0.85rem;'>
        <p>Research Assistant • Documentation Tool</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main app entry point."""
    init_session_state()
    display_header()
    display_sidebar()
    display_main_interface()
    display_footer()


if __name__ == "__main__":
    main()
