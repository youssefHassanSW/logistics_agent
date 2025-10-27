# 🚀 Streamlit UI Quick Start Guide

Get the Logistics Multi-Agent System UI up and running in 3 simple steps!

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Step 1: Install Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (UI framework)
- LangChain & LangGraph (Agent framework)
- Pandas (Data handling)
- And other required packages

## Step 2: Configure Your API Key

Create a file named `.env` in the project root directory with the following content:

```
ANTHROPIC_API_KEY=your-actual-api-key-here
```

**Important:** Replace `your-actual-api-key-here` with your real Anthropic API key.

## Step 3: Launch the Application

### Windows
Double-click the `run_streamlit.bat` file, or run in terminal:
```bash
run_streamlit.bat
```

### Linux/Mac
Make the script executable first:
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

### Or use Streamlit directly
```bash
streamlit run streamlit_app.py
```

## What Happens Next?

1. Your default web browser will automatically open
2. The app will be available at: `http://localhost:8501`
3. You'll see the System Visualization page

## Using the UI

### 🔍 System Visualization Page
- **View the multi-agent architecture graph**
- **Learn about each specialized agent**
- **Browse available logistics scenarios**

### ▶️ Scenario Runner Page
- **Select a scenario** from the dropdown (1-6 available)
- **Click "Run Scenario"** to execute
- **Watch real-time progress** as agents work
- **Review comprehensive results** with recommendations

## Example Scenarios

Try these scenarios to see the system in action:

1. **Scenario 1: Low Inventory Crisis**
   - Good for: First-time users
   - Shows: Inventory and procurement coordination

2. **Scenario 4: Cost Optimization Analysis**
   - Good for: Advanced users
   - Shows: Complex multi-agent coordination

3. **Scenario 5: Supplier Crisis**
   - Good for: Crisis management examples
   - Shows: Contingency planning across agents

## Troubleshooting

### "API Key Missing" Error
- **Problem:** `.env` file not found or incorrect
- **Solution:** Create `.env` file with `ANTHROPIC_API_KEY=your-key`
- **Verify:** Check the sidebar shows "✅ API Key Configured"

### "Graph Visualization Not Available"
- **Problem:** Graph image hasn't been generated
- **Solution:** Click "Generate Graph Visualization" button on the System Visualization page
- **Alternative:** Run `python main.py viz` in terminal

### Application Won't Start
- **Problem:** Dependencies not installed
- **Solution:** Run `pip install -r requirements.txt` again
- **Verify:** Check that streamlit is installed with `pip list | grep streamlit`

### Browser Doesn't Open Automatically
- **Problem:** Browser blocking or port already in use
- **Solution:** Manually open `http://localhost:8501` in your browser
- **Alternative:** Use a different port: `streamlit run streamlit_app.py --server.port 8502`

## Tips for Best Experience

1. **Start with System Visualization**
   - Familiarize yourself with the agent structure
   - Understand what each agent does

2. **Begin with Simple Scenarios**
   - Try Scenario 1 or 2 first
   - These have medium complexity

3. **Watch the Progress Bar**
   - See which agent is working in real-time
   - Understand the delegation flow

4. **Read the Final Summary**
   - Contains actionable recommendations
   - Shows business impact analysis

5. **Explore the Execution Log**
   - Expand to see detailed agent interactions
   - Understand decision-making process

## Next Steps

Once you're comfortable with the UI:

1. **Try Different Scenarios** - Each showcases different agent combinations
2. **Compare Results** - Run the same scenario multiple times
3. **Learn the Patterns** - Notice how agents collaborate
4. **Customize** - Modify scenarios or add new ones

## Getting Help

- **UI Issues:** Check browser console (F12) for errors
- **Scenario Issues:** Review the detailed execution log
- **API Issues:** Verify your API key has sufficient credits
- **General Questions:** See `STREAMLIT_README.md` for detailed documentation

## System Requirements

- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 100MB for dependencies
- **Network:** Internet connection for API calls
- **Browser:** Chrome, Firefox, Safari, or Edge (latest versions)

## Performance Notes

- First scenario run may take longer (system initialization)
- Complex scenarios (4, 5, 6) take more time
- Progress updates are real-time (no page refresh needed)
- Results are cached for review after execution

---

**Ready to go?** Run the app and explore the multi-agent system! 🚀

