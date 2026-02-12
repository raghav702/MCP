# Deployment Guide

## Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository

1. Make sure your `.env` file is NOT committed (it's already in `.gitignore`)
2. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

### Step 2: Push to GitHub

1. Create a new repository on GitHub (don't initialize with README)
2. Link your local repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch (main), and main file: `app.py`
5. Click "Advanced settings" and add secrets:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key"
   TAVILY_API_KEY = "your_tavily_api_key"
   DEBUG = "false"
   ```
6. Click "Deploy"

### Step 4: Wait for Deployment

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

---

## Environment Variables Required

- `GOOGLE_API_KEY` - Your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `TAVILY_API_KEY` - Your Tavily API key from [tavily.com](https://tavily.com)
- `DEBUG` - Set to "false" for production

---

## Local Development

1. Copy `.env.example` to `.env`
2. Add your API keys
3. Run: `streamlit run app.py`

---

## Troubleshooting

**App won't start:**
- Check that all secrets are configured in Streamlit Cloud dashboard
- Verify API keys are valid
- Check requirements.txt includes all dependencies

**Search not working:**
- Verify TAVILY_API_KEY is set correctly
- Check Tavily API quota (free tier: 1,000 searches/month)

**Gemini errors:**
- Verify GOOGLE_API_KEY is valid
- Make sure you're using `gemini-2.5-flash-lite` model
- Check API quota limits
