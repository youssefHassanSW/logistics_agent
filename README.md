# Logistics Multi-Agent System

**A supervisor/worker multi-agent system built with LangGraph's `langgraph-supervisor` package and Claude for handling complex logistics scenarios.**

## 🎯 Quick Start

### Option 1: Streamlit UI (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 3. Launch the UI
streamlit run streamlit_app.py
# Or double-click run_streamlit.bat (Windows) or run_streamlit.sh (Linux/Mac)
```

### Option 2: Command Line
```bash
# 1. Activate ML environment
conda activate ML

# 2. Set API key
set ANTHROPIC_API_KEY=your-key-here  # Windows
export ANTHROPIC_API_KEY=your-key    # Linux/Mac

# 3. Run a scenario
python main.py          # Interactive mode
python main.py 1        # Run scenario 1
python main.py list     # List all scenarios
```

## 📂 Project Structure (Refactored)

```
better_logistics_agent/
├── agents/                    # Individual agent definitions
│   ├── __init__.py
│   ├── route_planner.py
│   ├── procurement_manager.py
│   ├── inventory_manager.py
│   ├── distribution_handler.py
│   ├── demand_forecaster.py
│   └── cost_optimizer.py
│
├── config/                    # Configuration settings
│   ├── __init__.py
│   └── settings.py
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── state_filtering.py    # Message filtering
│   └── scenario_loader.py    # Scenario loading
│
├── tools/                     # 18 specialized agent tools
│   ├── __init__.py
│   ├── route_planner_tools.py
│   ├── procurement_tools.py
│   ├── inventory_tools.py
│   ├── distribution_tools.py
│   ├── forecaster_tools.py
│   └── cost_optimizer_tools.py
│
├── markdowns/                 # All documentation
│   ├── QUICKSTART.md
│   ├── USAGE_GUIDE.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── README_IMPLEMENTATION.md
│   └── PROJECT_OVERVIEW.md
│
├── mock_data/                 # 6 test scenarios
│   └── scenario_*/
│
├── streamlit_app.py           # Streamlit Web UI (NEW!)
├── run_streamlit.bat          # Windows launcher
├── run_streamlit.sh           # Linux/Mac launcher
├── STREAMLIT_README.md        # UI documentation
├── STREAMLIT_QUICKSTART.md    # UI quick start guide
├── main.py                    # Simplified entry point (using langgraph-supervisor)
├── test_graph_structure.py   # Structure tests
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## ✨ Key Features

### 🎨 Streamlit Web UI (New!)
- **System Visualization**: Interactive graph showing agent structure
- **Scenario Runner**: Beautiful interface for running logistics scenarios
- **Real-Time Progress**: Live progress bar and agent status updates
- **Comprehensive Results**: Formatted output with detailed execution logs

### 🔄 Refactored with langgraph-supervisor
- **Simplified Architecture**: Uses official `langgraph-supervisor` package
- **Auto-Generated Handoffs**: Automatic transfer tools for all agents
- **Built-in Graph Assembly**: No manual node/edge management
- **~80% Code Reduction**: Cleaner, more maintainable codebase

### 🤖 6 Specialized Agents
1. **Route Planner** - Route optimization & traffic management
2. **Procurement Manager** - Supplier management & purchasing
3. **Inventory Manager** - Stock monitoring & shortage prediction
4. **Distribution Handler** - Delivery management & SLA monitoring
5. **Demand Forecaster** - Demand prediction & trend analysis
6. **Cost Optimizer** - Financial analysis & cost reduction

### 📊 6 Test Scenarios
1. Low Inventory Crisis (MEDIUM complexity)
2. Route Disruption (MEDIUM complexity)
3. Demand Spike Forecast (HIGH complexity)
4. Cost Optimization (VERY HIGH complexity)
5. Supplier Crisis (HIGH complexity)
6. Distribution Delays & SLA (HIGH complexity)

## 🚀 Usage

### Run Tests (No API Key Needed)
```bash
python test_graph_structure.py
```

### Run Specific Scenario
```bash
python main.py 1    # Low Inventory Crisis
python main.py 4    # Cost Optimization Analysis
```

### Generate Graph Visualization
```bash
python main.py viz
```

## 📚 Documentation

### Streamlit UI Documentation
- **[STREAMLIT_QUICKSTART.md](markdowns/STREAMLIT_QUICKSTART.md)** - Get the UI running in 3 steps
- **[STREAMLIT_README.md](markdowns/STREAMLIT_README.md)** - Complete UI features and usage guide

### General Documentation
All documentation is in the `markdowns/` folder:

- **[QUICKSTART.md](markdowns/QUICKSTART.md)** - Get running in 3 steps
- **[USAGE_GUIDE.md](markdowns/USAGE_GUIDE.md)** - Complete usage instructions
- **[PROJECT_OVERVIEW.md](markdowns/PROJECT_OVERVIEW.md)** - High-level system description
- **[IMPLEMENTATION_SUMMARY.md](markdowns/IMPLEMENTATION_SUMMARY.md)** - Technical implementation details

## 🏗️ Architecture

### Supervisor/Worker Pattern

```
┌─────────────────────────┐
│   Main Orchestrator     │  ← langgraph-supervisor
│     (Supervisor)        │
└───────────┬─────────────┘
            │
    ┌───────┴───────┬──────────┬──────────┬──────────┬──────────┐
    │               │          │          │          │          │
┌───▼───┐     ┌────▼────┐ ┌──▼───┐  ┌───▼────┐ ┌──▼──┐   ┌───▼───┐
│ Route │     │Procure- │ │Inven-│  │Distri- │ │Demand│   │ Cost  │
│Planner│     │  ment   │ │tory  │  │bution  │ │Cast- │   │Optim- │
└───────┘     └─────────┘ └──────┘  └────────┘ └──────┘   └───────┘
```

### Key Design Decisions

1. **langgraph-supervisor**: Official prebuilt package for supervisor/worker pattern
2. **Modular Structure**: Each agent in separate file for better maintainability
3. **Token-Efficient**: State filtering removes CSV data while maintaining context
4. **Sequential Delegation**: Agents called one at a time for better control

## 🔧 Technical Stack

- **Framework**: LangGraph (with langgraph-supervisor)
- **LLM**: Claude 3.5 Sonnet (Anthropic)
- **Language**: Python 3.13
- **Environment**: Conda (ML environment)
- **Data Format**: CSV files in mock_data/

## 📈 Project Stats

- **Agents**: 6 specialized + 1 supervisor
- **Tools**: 18 CSV-reading tools
- **Scenarios**: 6 complete test scenarios
- **Code Reduction**: ~80% less boilerplate vs manual implementation
- **Tests**: Full structure test suite

## 🎓 Team Collaboration

The refactored structure makes team collaboration easier:

- **`agents/`**: Each team member can work on individual agents
- **`tools/`**: Tools organized by agent specialization
- **`config/`**: Centralized configuration management
- **`utils/`**: Shared utilities for common functionality
- **`markdowns/`**: All documentation in one place

## 🆚 What Changed in Refactoring?

### Before
```python
# orchestrator.py - Manual handoff tools (~140 lines)
# agents.py - All agents in one file (~160 lines)
# Manual graph assembly in main.py
```

### After
```python
# agents/ - Individual agent files (~30 lines each)
# main.py - Uses langgraph-supervisor (~200 lines, much simpler)
# No orchestrator.py needed!
```

### Benefits
✅ 80% less boilerplate code  
✅ Better code organization  
✅ Easier to extend with new agents  
✅ Follows official LangGraph patterns  
✅ More maintainable for teams  

## 🤝 Contributing

When adding new agents or tools:

1. Create new agent file in `agents/`
2. Add tools in `tools/` directory
3. Import agent in `agents/__init__.py`
4. Add to supervisor agents list in `main.py`

That's it! langgraph-supervisor handles the rest.

## 📝 License

This project demonstrates the langgraph-supervisor pattern for multi-agent coordination.

---

**Built with**: LangGraph + Claude 3.5 Sonnet  
**Architecture**: Supervisor/Worker (langgraph-supervisor)  
**Status**: Production Ready & Refactored  

