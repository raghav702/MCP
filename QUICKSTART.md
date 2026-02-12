# 🚀 Quick Start Guide

## Step-by-Step Setup (5 minutes)

### 1️⃣ Install Dependencies

Open PowerShell in this directory and run:

```powershell
pip install -r requirements.txt
```

This installs:
- LangGraph (agent orchestration)
- LangChain (LLM abstractions)
- OpenAI/Anthropic SDKs
- Pydantic (type safety)
- Other utilities

### 2️⃣ Configure API Key

**Option A: Using OpenAI (Recommended for testing)**

1. Get API key from: https://platform.openai.com/api-keys
2. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-proj-...your_key_here
   ```

**Option B: Using Anthropic Claude**

1. Get API key from: https://console.anthropic.com/
2. Edit `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...your_key_here
   ```

### 3️⃣ Run the Agent!

**Option A: Web UI (Recommended)**

```powershell
streamlit run app.py
```

- Opens browser automatically at http://localhost:8501
- Beautiful dashboard with progress tracking
- One-click export and history

**Option B: CLI Interface**

```powershell
python main.py
```

You'll see:
```
╔════════════════════════════════════════════════╗
║   Research Assistant Agent - MVP               ║
║   Powered by LangGraph + MCP                   ║
╚════════════════════════════════════════════════╝

Enter your research query: _
```

### 4️⃣ Try These Example Queries

- "What are the latest developments in AI agents?"
- "Compare State Space Models vs Transformers in 2026"
- "Explain the Model Context Protocol"
- "How does LangGraph work?"

## 🧪 Testing

Run automated test:

```powershell
python test_agent.py
```

## 📁 Output

Reports are saved to `reports/` folder as Markdown files with:
- Executive summary
- Detailed findings
- Key insights
- Full citations

## 🐛 Troubleshooting

**Issue: ModuleNotFoundError**
```powershell
pip install -r requirements.txt --upgrade
```

**Issue: API Key Error**
- Check `.env` file exists
- Verify API key is correct
- Make sure no extra spaces

**Issue: "No module named 'src'"**
- Make sure you're in the project root directory
- Python should see the `src/` folder

## 🔧 Configuration

Edit `src/config.py` to change:
- Number of search results
- Number of sources to fetch
- Enable/disable debug mode
- Switch LLM provider

## 🎯 What Just Happened?

When you run the agent:

1. **Planning Node**: Breaks your query into subtopics
2. **Search Node**: Searches for each subtopic (currently mocked)
3. **Fetch Node**: Gets full content from top sources
4. **Synthesis Node**: LLM generates comprehensive report
5. **Output Node**: Saves formatted report with citations

All orchestrated by **LangGraph**'s state machine!

## 🚀 Next Steps

1. Run with different queries to test
2. Check `reports/` folder for outputs
3. Enable DEBUG mode in `.env` to see workflow steps
4. Customize prompts in `src/agent_nodes.py`
5. Add real MCP servers (replace mock mode)

## 📊 Cost Estimate

With OpenAI GPT-4:
- ~2-3 API calls per research query
- ~$0.05 - $0.15 per report
- 10 test queries = ~$1-2

**You just built a working AI agent! 🎉**

---

Need help? Check [README.md](README.md) for full documentation.
