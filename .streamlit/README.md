# Streamlit Secrets Configuration

## Quick Setup

1. **Copy the template:**
   ```bash
   # Windows
   copy secrets.toml.example secrets.toml
   
   # Linux/Mac
   cp secrets.toml.example secrets.toml
   ```

2. **Edit `secrets.toml` and add your API keys:**
   ```toml
   ANTHROPIC_API_KEY = "your-actual-key-here"
   GOOGLE_API_KEY = "your-google-key-here"
   OPENAI_API_KEY = "your-openai-key-here"
   MODEL_PROVIDER = "claude"
   ```

3. **Start your app:**
   ```bash
   streamlit run streamlit_app.py
   ```

## ⚠️ Important

- **NEVER commit `secrets.toml`** - It contains your private API keys!
- `secrets.toml` is in `.gitignore` - keep it that way
- Only commit `secrets.toml.example` (the template)

## 📖 More Info

- [Complete Migration Guide](../SECRETS_MIGRATION_GUIDE.md)
- [Streamlit Secrets Documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-an-app/secrets-management)

