"""
Streamlit UI for Logistics Multi-Agent System

This application provides a visual interface for:
1. Visualizing the multi-agent system structure
2. Running logistics scenarios and viewing results
"""

import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from io import StringIO
import sys
from contextlib import contextmanager

# Load environment variables
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph_supervisor import create_supervisor

from config import MODEL_NAME, MOCK_DATA_DIR
from agents import (
    route_planner_agent,
    procurement_manager_agent,
    inventory_manager_agent,
    distribution_handler_agent,
    demand_forecaster_agent,
    cost_optimizer_agent,
)
from utils import load_scenario, list_available_scenarios
from main import create_logistics_graph


# Page configuration
st.set_page_config(
    page_title="Logistics Multi-Agent System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .scenario-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .agent-status {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .output-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #ddd;
        margin: 1rem 0;
        max-height: 600px;
        overflow-y: auto;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
</style>
""", unsafe_allow_html=True)


def load_scenario_index():
    """Load scenario index from CSV"""
    index_path = MOCK_DATA_DIR / "scenario_index.csv"
    if index_path.exists():
        return pd.read_csv(index_path)
    return None


def check_api_key():
    """Check if API key is set"""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def create_output_card(content: str, color: str = "#2E86AB") -> str:
    """Create a styled card for displaying final output."""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
        border-left: 5px solid {color};
        border-radius: 10px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="color: #333; line-height: 1.6;">
            {content}
        </div>
    </div>
    """


# Sidebar navigation
st.sidebar.title("🚚 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["System Visualization", "Scenario Runner"],
    label_visibility="collapsed"
)

# API Key Status in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
if check_api_key():
    st.sidebar.success("✅ API Key Configured")
else:
    st.sidebar.error("❌ API Key Missing")
    st.sidebar.info("Please set ANTHROPIC_API_KEY in your .env file")


# ============================================================================
# PAGE 1: SYSTEM VISUALIZATION
# ============================================================================
if page == "System Visualization":
    st.markdown('<div class="main-header">🔍 System Visualization</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This page provides an overview of the multi-agent logistics system architecture,
    showing how different specialized agents work together to handle logistics scenarios.
    """)
    
    # System Overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 System Architecture")
        
        # Check if graph visualization exists
        graph_path = Path("logistics_graph.png")
        if graph_path.exists():
            st.image(str(graph_path), caption="Multi-Agent System Graph", use_container_width=True)
        else:
            st.info("Graph visualization not available. Generate it using: `python main.py viz`")
            
            if st.button("🎨 Generate Graph Visualization", key="gen_graph"):
                with st.spinner("Generating graph visualization..."):
                    try:
                        from main import visualize_graph
                        visualize_graph()
                        st.success("✅ Graph generated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error generating graph: {e}")
    
    with col2:
        st.subheader("🤖 Agents")
        
        agents_info = [
            ("Route Planner", "🗺️", "Optimizes delivery routes and handles traffic disruptions"),
            ("Procurement Manager", "📦", "Manages supplier relationships and purchase orders"),
            ("Inventory Manager", "📊", "Monitors stock levels and reorder points"),
            ("Distribution Handler", "🚛", "Coordinates deliveries and manages SLAs"),
            ("Demand Forecaster", "📈", "Predicts demand spikes and trends"),
            ("Cost Optimizer", "💰", "Identifies cost-saving opportunities"),
        ]
        
        for name, emoji, desc in agents_info:
            with st.expander(f"{emoji} {name}"):
                st.write(desc)
    
    # System Workflow
    st.markdown("---")
    st.subheader("🔄 System Workflow")
    
    workflow_cols = st.columns(5)
    workflow_steps = [
        ("1️⃣", "Trigger Event", "Scenario event occurs"),
        ("2️⃣", "Orchestrator", "Analyzes situation"),
        ("3️⃣", "Agent Delegation", "Routes to specialists"),
        ("4️⃣", "Agent Processing", "Agents analyze & act"),
        ("5️⃣", "Final Summary", "Consolidated results"),
    ]
    
    for col, (num, title, desc) in zip(workflow_cols, workflow_steps):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">{num}</div>
                <div style="font-weight: bold; margin: 0.5rem 0;">{title}</div>
                <div style="font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Scenario Overview
    st.markdown("---")
    st.subheader("📋 Available Scenarios")
    
    scenario_df = load_scenario_index()
    if scenario_df is not None:
        # Display as formatted cards
        for _, row in scenario_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="scenario-card">
                    <h4>Scenario {row['scenario_id']}: {row['scenario_name']}</h4>
                    <p><strong>Severity:</strong> {row['severity']} | 
                       <strong>Complexity:</strong> {row['complexity']}</p>
                    <p><strong>Primary Agents:</strong> {row['primary_agents']}</p>
                    <p><strong>Key Metrics:</strong> {row['key_metrics']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Scenario index not found")


# ============================================================================
# PAGE 2: SCENARIO RUNNER
# ============================================================================
elif page == "Scenario Runner":
    st.markdown('<div class="main-header">▶️ Scenario Runner</div>', unsafe_allow_html=True)
    
    if not check_api_key():
        st.error("⚠️ Cannot run scenarios: ANTHROPIC_API_KEY not configured")
        st.info("Please set your Anthropic API key in the .env file to use this feature.")
        st.stop()
    
    # ========================================================================
    # SECTION 1: SCENARIO SELECTION AND EXECUTION
    # ========================================================================
    st.subheader("1️⃣ Scenario Selection")
    
    scenario_df = load_scenario_index()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if scenario_df is not None:
            scenario_options = [
                f"Scenario {row['scenario_id']}: {row['scenario_name']} (Severity: {row['severity']})"
                for _, row in scenario_df.iterrows()
            ]
            selected_scenario = st.selectbox(
                "Select a scenario to run:",
                options=range(len(scenario_options)),
                format_func=lambda x: scenario_options[x]
            )
            scenario_id = selected_scenario + 1
        else:
            st.error("Could not load scenarios")
            st.stop()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.button(
            "🚀 Run Scenario",
            type="primary"
        )
    
    # Show selected scenario details
    if scenario_df is not None:
        selected_row = scenario_df.iloc[selected_scenario]
        st.markdown(f"""
        <div class="scenario-card">
            <h4>{selected_row['scenario_name']}</h4>
            <p><strong>Complexity:</strong> {selected_row['complexity']} | 
               <strong>Severity:</strong> {selected_row['severity']} | 
               <strong>Trigger:</strong> {selected_row['trigger_type']}</p>
            <p><strong>Primary Agents:</strong> {selected_row['primary_agents']}</p>
            <p><strong>Key Metrics:</strong> {selected_row['key_metrics']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 2: PROGRESS BAR AND CURRENT AGENT
    # ========================================================================
    st.subheader("2️⃣ Execution Progress")
    
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_box = st.empty()
        status_box.info("ℹ️ Ready to run scenario. Click 'Run Scenario' to start.")
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 3: OUTPUT SECTION
    # ========================================================================
    st.subheader("3️⃣ Execution Results")
    
    output_container = st.container()
    
    # ========================================================================
    # RUN SCENARIO LOGIC
    # ========================================================================
    if run_button:
        with output_container:
            # Scenario details expander
            scenario_details_container = st.empty()
            
            # Results container
            results_container = st.container()
        
        try:
            # Load scenario
            scenario = load_scenario(scenario_id)
            
            if not scenario:
                st.error(f"Failed to load scenario {scenario_id}")
                st.stop()
            
            # Display scenario details
            with scenario_details_container:
                with st.expander("📄 Scenario Details", expanded=False):
                    st.markdown(f"**Event Type:** {scenario['trigger_event'].get('event_type', 'N/A')}")
                    st.markdown(f"**Severity:** {scenario['trigger_event'].get('severity', 'N/A')}")
                    st.markdown(f"**Description:**")
                    st.text(scenario['trigger_event'].get('description', 'N/A'))
            
            # Create and run the graph
            graph = create_logistics_graph()
            
            initial_state = {
                "messages": [HumanMessage(content=scenario['message'])]
            }
            
            all_messages = []
            step_count = 0
            total_steps = 10  # Estimate, will adjust dynamically
            
            # Stream execution
            for state in graph.stream(initial_state):
                step_count += 1
                
                if state:
                    node_name = list(state.keys())[0]
                    
                    # Update progress
                    progress_value = min(step_count / total_steps, 0.95)
                    progress_bar.progress(progress_value)
                    
                    status_box.markdown(
                        f'<div class="agent-status">🔄 Step {step_count}: {node_name}</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Extract message
                    node_state = state[node_name]
                    if "messages" in node_state:
                        messages = node_state["messages"]
                        if messages:
                            latest_msg = messages[-1]
                            if hasattr(latest_msg, 'content') and latest_msg.content:
                                all_messages.append({
                                    'step': step_count,
                                    'node': node_name,
                                    'content': latest_msg.content
                                })
                
                final_state = state
            
            # Complete progress
            progress_bar.progress(1.0)
            status_box.success("✅ Scenario execution completed!")
            
            # Extract final summary
            summary = None
            if final_state:
                last_key = list(final_state.keys())[-1]
                if "messages" in final_state[last_key]:
                    messages = final_state[last_key]["messages"]
                    for msg in reversed(messages):
                        if hasattr(msg, 'content') and msg.content and len(str(msg.content).strip()) > 50:
                            summary = msg.content
                            break
            
            # Display results directly
            with results_container:
                # Show step-by-step execution log first
                with st.expander("🔍 Detailed Execution Log", expanded=False):
                    for msg in all_messages:
                        st.markdown(f"**[Step {msg['step']}] {msg['node']}**")
                        st.text(msg['content'][:500] + "..." if len(msg['content']) > 500 else msg['content'])
                        st.markdown("---")
                
                # Then show final model output in a styled card
                st.markdown("### 📋 Final Agent Output")
                if summary:
                    # Convert markdown to HTML for proper rendering in the card
                    import markdown
                    html_content = markdown.markdown(summary)
                    card_html = create_output_card(html_content, color="#2E86AB")
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    st.warning("No final summary generated")
            
        except Exception as e:
            st.error(f"❌ Error during scenario execution: {e}")
            import traceback
            st.code(traceback.format_exc())


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Logistics Multi-Agent System</p>
    <p>Powered by LangGraph & Claude</p>
</div>
""", unsafe_allow_html=True)

