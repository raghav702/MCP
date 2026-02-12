# 🌐 Streamlit Web UI Guide

**Complete guide for running and customizing the Streamlit interface**

---

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install streamlit
# Or reinstall all dependencies
pip install -r requirements.txt
```

### 2. Run the App

```powershell
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🎨 Features

### Main Interface
- **🔍 Search Bar** - Enter any research query
- **💡 Example Queries** - Quick-start buttons with sample topics
- **📊 Progress Tracker** - Real-time workflow visualization
- **🎯 Stage Indicators** - Visual progress through 5 stages

### Report Display
- **📄 Full Report Tab** - Markdown-formatted research report
- **🔬 Subtopics Tab** - Shows how query was decomposed
- **📚 Citations Tab** - All sources with URLs
- **💾 Export Tab** - Download as MD, JSON, or view file path

### Sidebar
- **📖 About** - Quick project description
- **📊 How It Works** - 5-stage workflow explanation
- **🛠️ Tech Stack** - Technologies used
- **📚 Research History** - Last 5 queries with quick access

### Metrics Dashboard
- **Sources Analyzed** - Number of sources found
- **Subtopics Identified** - Query breakdown count
- **Citations Generated** - Reference count
- **Average Duration** - Execution time

---

## 🎯 Usage Examples

### Basic Research
1. Enter query: "What are AI agents?"
2. Click "🚀 Research"
3. Watch progress bars
4. View formatted report

### Using Examples
1. Click any example query button
2. Automatically starts research
3. No typing needed!

### Export Results
1. Complete a research query
2. Go to "💾 Export" tab
3. Download as Markdown or JSON
4. Or find file path to saved report

---

## 🎨 Customization

### Change Colors

Edit the CSS in `app.py`:

```python
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        # Change these hex colors!
    }
</style>
```

### Add More Example Queries

In `display_main_interface()`:

```python
examples = [
    "Your custom query 1",
    "Your custom query 2",
    "Your custom query 3"
]
```

### Modify Layout

Change to narrow layout:

```python
st.set_page_config(
    layout="wide",  # Change to "centered"
)
```

---

## 🔧 Configuration

### Environment Variables

Same `.env` file as CLI:

```bash
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here

DEBUG=true  # Enable debug mode
```

### Port Configuration

Run on different port:

```powershell
streamlit run app.py --server.port 8502
```

### Theme Customization

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 📱 Features Breakdown

### Progress Visualization

Shows 5 stages visually:
1. 🧠 Planning (20%)
2. 🔍 Searching (40%)
3. 📥 Fetching (60%)
4. ✍️ Synthesizing (80%)
5. 💾 Saving (100%)

### Research History

- Stores last 5 queries in session
- Quick access to previous reports
- Shows timestamp and source count
- Click "View Report" to reload

### Export Options

**Markdown Export:**
- Full report with formatting
- Citations at bottom
- Ready to share

**JSON Export:**
- Structured data
- All metadata included
- API-friendly format

---

## 🎬 Demo Tips

### For Screen Recording

1. **Use Full Screen** - `F11` for immersive view
2. **Clear History** - Restart app for clean demo
3. **Use Examples** - One-click queries are impressive
4. **Show Tabs** - Demonstrate all report sections

### For Screenshots

1. **Capture Query Input** - Show clean interface
2. **Progress Animation** - Mid-execution screenshot
3. **Metrics Dashboard** - After completion
4. **Full Report** - Formatted output
5. **Citations View** - Source tracking

### For Live Demo

1. **Prepare Query** - Test beforehand
2. **Enable Debug** - Show workflow steps
3. **Narrate Stages** - Explain as it runs
4. **Show Export** - Download functionality
5. **Access History** - Previous queries

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
```powershell
git add .
git commit -m "Add Streamlit UI"
git push
```

2. **Deploy**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect GitHub repo
- Select `app.py`
- Add secrets (API keys)
- Deploy!

3. **Add Secrets**
In Streamlit Cloud dashboard:
```toml
OPENAI_API_KEY = "your_key_here"
```

### Alternative: Local Network Access

Share on local network:

```powershell
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices: `http://YOUR_IP:8501`

---

## 🐛 Troubleshooting

### "Module not found: streamlit"

```powershell
pip install streamlit
```

### App won't start

```powershell
# Check if port is available
netstat -ano | findstr :8501

# Use different port
streamlit run app.py --server.port 8502
```

### API Key Error

1. Check `.env` file exists
2. Verify key is correct
3. No extra spaces or quotes
4. Restart Streamlit app

### Slow Performance

1. Check API rate limits
2. Enable caching:
```python
@st.cache_data
def run_research(query):
    # ...
```

### Session State Issues

Clear cache:
```powershell
streamlit cache clear
```

---

## 📊 Performance Tips

### Caching

Add to top of `app.py`:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def run_research(query: str):
    # This will cache results
    return asyncio.run(run_research_async(query))
```

### Async Improvements

For better responsiveness, use Streamlit's async support:

```python
import asyncio

async def main_async():
    # Your async code here
    pass

asyncio.run(main_async())
```

---

## 🎨 UI Enhancements

### Add Animations

```python
import time

with st.spinner("Researching..."):
    time.sleep(1)  # Simulate work
    st.success("Done!")
```

### Add Charts

```python
import plotly.express as px

fig = px.bar(
    x=["Planning", "Search", "Fetch", "Synthesis", "Output"],
    y=[5, 8, 4, 12, 3]
)
st.plotly_chart(fig)
```

### Add Images

```python
from PIL import Image

st.image("architecture.png", caption="System Architecture")
```

---

## 📚 Next Steps

### Enhancements to Add

1. **User Authentication** - Login system
2. **Database Backend** - Persistent storage
3. **API Integration** - REST API wrapper
4. **Real-time Streaming** - Live LLM output
5. **Collaborative Research** - Multi-user support

### Portfolio Additions

1. **Demo Video** - Record using Streamlit
2. **Live Deployment** - Share URL
3. **Screenshots** - Add to README
4. **Blog Post** - Write about building it

---

## ✅ Checklist

Before showing recruiters:

- [ ] Test all features work
- [ ] Add your branding/name
- [ ] Update links in footer
- [ ] Test on different browsers
- [ ] Deploy to Streamlit Cloud
- [ ] Add screenshots to README
- [ ] Record demo video
- [ ] Test with real API key

---

## 🔗 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Community](https://discuss.streamlit.io)
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud)

---

**Your professional web UI is ready! 🎉**

Run it now:
```powershell
streamlit run app.py
```
