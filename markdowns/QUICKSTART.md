# Quick Start Guide

## Get Running in 3 Steps

### Step 1: Activate Environment
```bash
conda activate ML
```

### Step 2: Set API Key

**Windows:**
```bash
set ANTHROPIC_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

### Step 3: Run a Scenario
```bash
python main.py
```

That's it! The system will guide you through selecting and running scenarios.

## Quick Commands

```bash
# Run specific scenario
python main.py 1    # Low Inventory Crisis

# List all scenarios
python main.py list

# Test system (no API key needed)
python test_graph_structure.py

# Generate graph visualization
python main.py viz
```

## What to Expect

When you run a scenario:

1. **Scenario Info**: Shows the logistics problem
2. **Agent Execution**: See which agents are working
3. **Final Summary**: Get actionable recommendations

Example output:
```
LOGISTICS SCENARIO ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Event Type: LOW_INVENTORY
Severity: HIGH
Scenario: scenario_1_low_inventory

[Orchestrator analyzes and delegates to agents]

FINAL SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: Critical inventory shortage for 5 products...
Actions Taken:
- Inventory Manager identified products below reorder point
- Procurement Manager recommended purchase orders...
Recommendations: Place urgent orders for...
```

## Available Scenarios

1. Low Inventory Crisis (MEDIUM)
2. Route Disruption (MEDIUM)
3. Demand Spike Forecast (HIGH)
4. Cost Optimization (VERY HIGH)
5. Supplier Crisis (HIGH)
6. Distribution Delays (HIGH)

## Troubleshooting

**"API key not set"**
→ Follow Step 2 above

**"Import errors"**
→ Ensure you're in ML environment: `conda activate ML`

**"Scenario not found"**
→ Use `python main.py list` to see valid IDs (1-6)

## Documentation

- `USAGE_GUIDE.md` - Comprehensive usage instructions
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `README_IMPLEMENTATION.md` - Architecture and design

## Testing (No API Key Required)

Verify everything works:
```bash
python test_graph_structure.py
```

Should show:
```
[PASS] Tools Import
[PASS] Agents Creation
[PASS] Scenario Loading
[PASS] Graph Structure
```

## First Run Recommendation

Start with Scenario 1 (Low Inventory Crisis):
```bash
python main.py 1
```

It's a simple 2-agent scenario that demonstrates the system clearly.

## Need Help?

1. Check `USAGE_GUIDE.md` for detailed instructions
2. Run tests: `python test_graph_structure.py`
3. Review mock data in `mock_data/` directories
4. Check the graph visualization: `python main.py viz`

