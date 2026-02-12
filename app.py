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
    page_title="Research Assistant Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(to right, #667eea, #764ba2);
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
    st.markdown('<h1 class="main-header">🤖 Research Assistant Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Research Automation with LangGraph & MCP</p>', unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with info and history."""
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.info("""
        This AI agent autonomously:
        - 🧠 Plans research strategy
        - 🔍 Searches multiple sources
        - 📥 Fetches full content
        - ✍️ Synthesizes findings
        - 💾 Saves with citations
        """)
        
        st.markdown("### 📊 How It Works")
        st.markdown("""
        1. **Planning** - Breaks query into subtopics
        2. **Search** - Finds relevant sources
        3. **Fetch** - Reads full articles
        4. **Synthesis** - Generates report
        5. **Output** - Saves with citations
        """)
        
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - LangGraph (Orchestration)
        - MCP Protocol (Tools)
        - OpenAI/Anthropic (LLM)
        - Pydantic (Type Safety)
        - AsyncIO (Performance)
        - Streamlit (Frontend)
        """)
        
        st.markdown("---")
        
        # Research History
        if st.session_state.research_history:
            st.markdown("### 📚 Research History")
            for i, item in enumerate(reversed(st.session_state.research_history[-5:])):
                with st.expander(f"🔍 {item['query'][:40]}..."):
                    st.caption(f"🕐 {item['timestamp']}")
                    st.caption(f"📄 {len(item.get('citations', []))} sources")
                    if st.button(f"View Report", key=f"view_{i}"):
                        st.session_state.current_report = item


def display_main_interface():
    """Display main research interface."""
    
    # Query input
    st.markdown("### 🔍 Start Your Research")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your research query:",
            placeholder="e.g., What are the latest developments in AI agents in 2026?",
            label_visibility="collapsed"
        )
    
    with col2:
        research_button = st.button("🚀 Research", type="primary", use_container_width=True)
    
    # Example queries
    st.markdown("**💡 Example Queries:**")
    examples = [
        "Compare State Space Models vs Transformers in 2026",
        "Explain the Model Context Protocol and its benefits",
        "What are the best practices for agentic AI in 2026?"
    ]
    
    example_cols = st.columns(3)
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(f"📝 {example[:40]}...", key=f"example_{i}", use_container_width=True):
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
    st.markdown(f"### 🔬 Researching: *{query}*")
    
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        ("🧠 Planning", "Breaking down query into subtopics...", 20),
        ("🔍 Searching", "Finding relevant sources...", 40),
        ("📥 Fetching", "Reading full article content...", 60),
        ("✍️ Synthesizing", "Generating comprehensive report...", 80),
        ("💾 Saving", "Finalizing report with citations...", 100)
    ]
    
    # Create placeholder for stages
    stage_container = st.container()
    
    with stage_container:
        stage_cols = st.columns(5)
        stage_indicators = []
        for i, (emoji, stage_name, _) in enumerate(stages):
            with stage_cols[i]:
                indicator = st.empty()
                stage_indicators.append(indicator)
                indicator.markdown(f"{emoji}\n\n{stage_name.split()[0]}", unsafe_allow_html=True)
    
    try:
        # Run research
        with st.spinner("🤖 AI Agent is working..."):
            # Simulate progress updates (in real implementation, hook into workflow)
            for i, (emoji, stage_name, progress) in enumerate(stages):
                status_text.markdown(f"**{emoji} {stage_name}**")
                progress_bar.progress(progress)
                
                # Highlight current stage
                for j, indicator in enumerate(stage_indicators):
                    if j == i:
                        indicator.markdown(f"✅ **{stages[j][0]}**", unsafe_allow_html=True)
                    elif j < i:
                        indicator.markdown(f"✅ {stages[j][0]}", unsafe_allow_html=True)
                
                # Execute research on last stage
                if i == len(stages) - 1:
                    final_state = run_research(query)
            
            progress_bar.progress(100)
            status_text.markdown("**✅ Research Complete!**")
        
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
        
        st.success("✅ Research completed successfully!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error during research: {str(e)}")
        st.exception(e)


def display_report(report: dict):
    """Display research report."""
    st.markdown("---")
    st.markdown("## 📄 Research Report")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>📚</h2>
            <h3>{}</h3>
            <p>Sources</p>
        </div>
        """.format(report.get('sources', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🔍</h2>
            <h3>{}</h3>
            <p>Subtopics</p>
        </div>
        """.format(len(report.get('subtopics', []))), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📝</h2>
            <h3>{}</h3>
            <p>Citations</p>
        </div>
        """.format(len(report.get('citations', []))), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>⏱️</h2>
            <h3>~30s</h3>
            <p>Duration</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Report tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Report", "🔬 Subtopics", "📚 Citations", "💾 Export"])
    
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
                label="📥 Download Markdown",
                data=report_md,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            # Download as JSON
            report_json = json.dumps(report, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=report_json,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # View saved file
            if report.get('output_path'):
                st.info(f"📁 Saved to:\n`{report['output_path']}`")
        
        st.markdown("---")
        st.markdown("**💡 Tip:** Reports are automatically saved to the `reports/` folder")


def display_footer():
    """Display footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>🤖 Research Assistant Agent</strong></p>
        <p>Built with LangGraph • MCP Protocol • Streamlit</p>
        <p>
            <a href='https://github.com/yourusername/project'>GitHub</a> • 
            <a href='#'>Documentation</a> • 
            <a href='#'>Portfolio</a>
        </p>
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
