# 🎨 Streamlit UI Features Guide

## Overview

The Streamlit UI provides a modern, intuitive interface for interacting with the Logistics Multi-Agent System. This document explains all the features and UI elements in detail.

---

## 🏠 Page 1: System Visualization

### Purpose
Understand the multi-agent system architecture before running scenarios.

### Sections

#### 1. System Architecture Graph
**Location:** Left side, main section

**What You See:**
- Visual representation of the agent network
- Supervisor node at the top
- 6 specialized agent nodes
- Connection lines showing delegation paths

**Features:**
- **Auto-generation:** Click "Generate Graph Visualization" if not present
- **High resolution:** Mermaid diagram format
- **Clear labeling:** All agents and connections labeled

**Use Case:** Understand how agents connect and communicate

---

#### 2. Agent List
**Location:** Right sidebar

**What You See:**
- 6 expandable cards, one per agent
- Agent emoji identifier
- Agent role description

**Features:**
- **Expandable details:** Click to see full agent description
- **Quick reference:** See all agents at a glance

**Agents Included:**
1. 🗺️ **Route Planner** - Route optimization
2. 📦 **Procurement Manager** - Supplier management
3. 📊 **Inventory Manager** - Stock monitoring
4. 🚛 **Distribution Handler** - Delivery coordination
5. 📈 **Demand Forecaster** - Predictive analytics
6. 💰 **Cost Optimizer** - Financial analysis

---

#### 3. System Workflow
**Location:** Below the graph

**What You See:**
- 5 colored gradient cards in a row
- Each card shows one workflow step

**Workflow Steps:**
1. **Trigger Event** - Scenario event occurs
2. **Orchestrator** - Analyzes the situation
3. **Agent Delegation** - Routes to specialists
4. **Agent Processing** - Agents analyze and act
5. **Final Summary** - Consolidated results

**Use Case:** Understand the end-to-end process flow

---

#### 4. Available Scenarios
**Location:** Bottom section

**What You See:**
- 6 styled scenario cards
- Each card contains:
  - Scenario ID and name
  - Severity level
  - Complexity rating
  - Primary agents involved
  - Key metrics

**Features:**
- **Color-coded severity:** Visual indication of urgency
- **Complete metadata:** All scenario details at a glance
- **Clickable:** Ready to switch to Scenario Runner

**Example Card:**
```
Scenario 1: Low Inventory Crisis
Severity: HIGH | Complexity: MEDIUM
Primary Agents: Inventory Manager | Procurement Manager
Key Metrics: 5 products below reorder | Revenue impact: Medium
```

---

## ▶️ Page 2: Scenario Runner

### Purpose
Execute logistics scenarios and view real-time results.

---

### Section 1: Scenario Selection

**UI Elements:**
- **Dropdown Menu:** Select from 6 scenarios
- **Run Button:** Execute the selected scenario
- **Scenario Details Card:** Shows selected scenario metadata

**Features:**

#### Dropdown Menu
- **Format:** "Scenario X: Name (Severity: LEVEL)"
- **Sorting:** Organized by scenario ID (1-6)
- **Disabled During Execution:** Prevents changing scenarios mid-run

#### Scenario Details Card
**Shows:**
- Scenario name
- Complexity and severity
- Trigger type
- Primary agents
- Key metrics
- Revenue/cost impact

**Styling:**
- Light blue background
- Blue left border
- Clear typography hierarchy

#### Run Button
- **Label:** "🚀 Run Scenario"
- **Color:** Blue (primary action)
- **States:**
  - Active: Clickable, blue background
  - Disabled: Grayed out during execution
  - Hover: Darker blue

---

### Section 2: Execution Progress

**Purpose:** Show real-time execution status

**UI Elements:**

#### Progress Bar
- **Type:** Linear progress indicator
- **Color:** Blue gradient
- **Range:** 0% to 100%
- **Updates:** Real-time as agents execute

**Behavior:**
- Starts at 0% when execution begins
- Increments with each agent step
- Reaches 100% when complete
- Smooth animation

#### Status Box
**Shows:**
- Current agent name
- Step number
- Status emoji (🔄 for running, ✅ for complete)

**Example Messages:**
```
🔄 Step 3: inventory_manager
```
```
✅ Scenario execution completed!
```

**Styling:**
- Light blue background
- Green left border
- Bold text
- Icon for visual feedback

**Updates:**
- Real-time (no page refresh)
- Smooth transitions
- Clear visual hierarchy

---

### Section 3: Execution Results

**Purpose:** Display final output and detailed logs

**UI Elements:**

#### Scenario Details Expander
- **Default:** Collapsed
- **Contains:**
  - Event type
  - Severity
  - Full description from trigger_event.csv

**Use Case:** Review input data before analyzing results

---

#### Results Display Box
**Contains:**
- Final summary heading
- Natural language analysis
- Actionable recommendations
- Business impact assessment

**Features:**
- **White background:** Clear contrast
- **Bordered box:** Distinct from other content
- **Scrollable:** Handles long outputs (max 600px height)
- **Formatted markdown:** Headings, lists, emphasis

**Example Content:**
```
📋 Final Summary

Issue: Inventory levels critically low for 5 products...

Actions Taken:
1. Inventory Manager: Identified shortages...
2. Procurement Manager: Generated purchase orders...

Recommendations:
- Expedite delivery for top priority items
- Review reorder points to prevent future shortages
- Estimated recovery time: 3-5 days
```

---

#### Detailed Execution Log
**Location:** Expandable section below results

**Contains:**
- Step-by-step agent interactions
- Full message content from each agent
- Node names and step numbers

**Features:**
- **Collapsible:** Expanded only when needed
- **Chronological order:** Step 1 to final step
- **Truncated previews:** First 500 characters per message
- **Separator lines:** Clear visual breaks between steps

**Use Case:** 
- Debug execution issues
- Understand agent reasoning
- Learn system behavior

---

## 🎨 Design Elements

### Color Scheme
- **Primary Blue:** `#1f77b4` - Headers, buttons, borders
- **Light Blue:** `#e8f4f8` - Status boxes, backgrounds
- **Gray:** `#f0f2f6` - Scenario cards
- **Gradient:** Purple gradient for metric cards
- **Green:** `#4CAF50` - Success indicators
- **Red:** Error states (if applicable)

### Typography
- **Headers:** 2.5rem, bold, center-aligned
- **Subheaders:** 1.5rem, bold
- **Body Text:** 1rem, standard weight
- **Code/Data:** Monospace font

### Spacing
- **Card Padding:** 1.5rem
- **Section Margins:** 1rem top/bottom
- **Border Width:** 2-5px depending on element
- **Border Radius:** 5-10px for rounded corners

---

## 🔄 Interactive Features

### Real-Time Updates
- **No Page Refresh:** All updates happen live
- **Smooth Animations:** Progress bar, status changes
- **Instant Feedback:** Button clicks, expansions

### State Management
- **Session Persistence:** Results stay visible after execution
- **Button States:** Disabled during execution
- **Error Handling:** Clear error messages with troubleshooting

### Navigation
- **Sidebar Radio:** Switch between pages instantly
- **Scroll Management:** Auto-scroll to important sections
- **Expander Memory:** Keeps state during execution

---

## 🔍 User Experience Details

### Loading States
- **Button:** Changes to disabled state
- **Progress Bar:** Animates smoothly
- **Status Box:** Updates every step
- **Spinner:** (Not used - progress bar is sufficient)

### Error States
- **API Key Missing:** Red alert in sidebar + scenario page
- **Execution Error:** Red error box with traceback
- **File Not Found:** Yellow warning with instructions

### Success States
- **Completion:** Green success message
- **Results:** Formatted output in white box
- **Clear Actions:** Next steps visible

---

## 📱 Responsive Design

### Desktop (Default)
- **Two-column layouts:** Graph + Agents
- **Wide progress bars:** Full width
- **Readable text:** Optimal line length

### Tablet/Mobile
- **Stacked layouts:** Vertical arrangement
- **Full-width elements:** Touch-friendly
- **Collapsible sidebar:** More screen space

---

## 🎯 Best Practices for Using the UI

### First Time Users
1. Start on **System Visualization** page
2. Review all agents and their roles
3. Read through available scenarios
4. Switch to **Scenario Runner**
5. Try **Scenario 1** (simplest)

### Regular Use
1. Go directly to **Scenario Runner**
2. Select desired scenario
3. Click **Run Scenario**
4. Watch progress bar
5. Review results
6. Check detailed log if needed

### Debugging/Learning
1. Run a scenario
2. Expand **Detailed Execution Log**
3. Follow step-by-step agent interactions
4. Understand decision-making process

---

## 🔧 Customization Options

### For Developers

#### Change Colors
Edit CSS in `streamlit_app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #YOUR_COLOR;
    }
</style>
""", unsafe_allow_html=True)
```

#### Modify Layout
Adjust column ratios:
```python
col1, col2 = st.columns([3, 1])  # 3:1 ratio
```

#### Add New Elements
Use Streamlit components:
```python
st.metric(label="Scenarios Run", value=5)
st.chart(data)
st.dataframe(df)
```

---

## 🚀 Performance Notes

### Fast Operations
- Page switching (instant)
- Scenario selection (instant)
- Expander toggle (instant)

### Moderate Operations
- Scenario execution (10-60 seconds)
- Progress updates (real-time)
- Result rendering (<1 second)

### One-Time Operations
- Graph generation (3-5 seconds)
- Initial load (1-2 seconds)

---

## 📊 UI Metrics

### Interaction Points
- **2 Pages:** System Visualization, Scenario Runner
- **1 Dropdown:** Scenario selection
- **1 Button:** Run scenario
- **3+ Expanders:** Details, logs, agents
- **1 Progress Bar:** Execution tracking
- **1 Status Box:** Current agent

### Visual Elements
- **6 Agent Cards:** With descriptions
- **6 Scenario Cards:** With metadata
- **5 Workflow Steps:** Visual process
- **1 Graph Image:** System architecture

---

## 💡 Tips & Tricks

### Speed Up Workflow
- Bookmark `http://localhost:8501` for quick access
- Use keyboard shortcuts (Tab, Enter) for navigation
- Collapse expanders you don't need

### Better Visibility
- Zoom browser for larger text
- Use fullscreen mode (F11)
- Adjust window width for optimal card display

### Understanding Results
- Read final summary first
- Then check detailed log for specifics
- Compare results across multiple runs

---

## 🎓 Learning Resources

### Understand the UI
- Read this document (UI_FEATURES.md)
- Follow STREAMLIT_QUICKSTART.md
- Review STREAMLIT_README.md

### Understand the System
- Check PROJECT_OVERVIEW.md
- Read IMPLEMENTATION_SUMMARY.md
- Review agent source code in `agents/`

---

**Questions?** Check the troubleshooting section in STREAMLIT_QUICKSTART.md or STREAMLIT_README.md

