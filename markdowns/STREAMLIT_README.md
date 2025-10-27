# Streamlit UI for Logistics Multi-Agent System

This is a comprehensive web-based user interface for the Logistics Multi-Agent System, built with Streamlit.

## Features

### 📊 Two Main Pages

#### 1. System Visualization
- **System Architecture Diagram**: Visual representation of the multi-agent graph
- **Agent Information**: Details about each specialized agent and their roles
- **System Workflow**: Step-by-step visualization of how scenarios are processed
- **Scenario Overview**: Complete list of available scenarios with metadata

#### 2. Scenario Runner
Three main UI sections:

1. **Scenario Selection & Execution**
   - Dropdown menu to select from 6 available scenarios
   - Detailed information about each scenario (severity, complexity, key metrics)
   - Run button to execute the selected scenario

2. **Progress Tracking**
   - Real-time progress bar showing execution progress
   - Live status updates showing which agent is currently working
   - Step-by-step tracking of the multi-agent workflow

3. **Results Display**
   - Final agent output with formatted summary
   - Comprehensive analysis of the logistics scenario
   - Detailed execution log (expandable)

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   
   Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Running the Application

### Windows
Double-click `run_streamlit.bat` or run in terminal:
```bash
run_streamlit.bat
```

### Linux/Mac
Make the script executable and run:
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

### Manual Start
```bash
streamlit run streamlit_app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

## Usage Guide

### System Visualization Page

1. **View System Architecture**
   - The graph visualization shows all agents and their connections
   - If the graph image doesn't exist, click "Generate Graph Visualization"

2. **Explore Agents**
   - Click on each agent card to see detailed information
   - Understand what each agent specializes in

3. **Review Scenarios**
   - Browse all available scenarios
   - See complexity levels, severity ratings, and key metrics

### Scenario Runner Page

1. **Select a Scenario**
   - Use the dropdown menu to choose a scenario (1-6)
   - Review the scenario details displayed below

2. **Execute the Scenario**
   - Click "🚀 Run Scenario" to start execution
   - Watch the progress bar and agent status updates in real-time

3. **View Results**
   - Read the final summary with recommendations
   - Expand the "Detailed Execution Log" to see step-by-step agent interactions

## Features Highlights

### Real-Time Progress Tracking
- The progress bar updates as each agent processes the scenario
- Current agent name is displayed in a highlighted status box
- Step counter shows progress through the workflow

### Beautiful UI Design
- Modern, responsive design with custom styling
- Color-coded severity levels and status indicators
- Card-based layout for easy information scanning
- Smooth animations and transitions

### Error Handling
- API key validation before scenario execution
- Clear error messages with troubleshooting information
- Graceful handling of execution failures

## Architecture

The Streamlit app integrates with the existing multi-agent system:

```
streamlit_app.py
    ↓
main.py (create_logistics_graph)
    ↓
langgraph_supervisor
    ↓
6 Specialized Agents
    ↓
Tools & Data Sources
```

## Troubleshooting

### API Key Issues
- **Error**: "API Key Missing"
- **Solution**: Create a `.env` file with `ANTHROPIC_API_KEY=your-key`

### Graph Visualization Not Showing
- **Error**: Graph image not found
- **Solution**: Click "Generate Graph Visualization" button or run `python main.py viz`

### Scenario Execution Fails
- **Error**: Various execution errors
- **Solution**: Check the detailed execution log for specific error messages

## Customization

### Changing Colors/Theme
Edit the CSS section in `streamlit_app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;  /* Change this color */
        ...
    }
</style>
""", unsafe_allow_html=True)
```

### Adding New Scenarios
1. Add scenario data to `mock_data/scenario_X_description/`
2. Update `mock_data/scenario_index.csv`
3. The UI will automatically pick up the new scenario

## Technical Details

### State Management
- Uses Streamlit's session state to track:
  - Running status
  - Current step/agent
  - Output results
  - Execution history

### Streaming Execution
- Real-time streaming of agent execution
- Progressive updates without page reload
- Efficient memory usage with lazy evaluation

### Performance
- Optimized for scenarios with 5-15 agent interactions
- Progress bar estimates based on typical workflow length
- Cached scenario metadata for faster loading

## Future Enhancements

Potential improvements:
- [ ] Export results to PDF/CSV
- [ ] Comparison view for multiple scenario runs
- [ ] Custom scenario builder
- [ ] Historical run database
- [ ] Performance metrics dashboard
- [ ] Agent utilization statistics

## Support

For issues or questions:
1. Check the execution log in the UI
2. Review error messages in the console
3. Verify all dependencies are installed
4. Ensure API key is correctly configured

## License

Same license as the main Logistics Multi-Agent System project.

