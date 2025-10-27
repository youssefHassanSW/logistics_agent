"""
Test script to verify Streamlit UI setup without running the full application.
This checks imports and basic functionality.
"""

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from langchain_anthropic import ChatAnthropic
        print("✅ LangChain Anthropic imported successfully")
    except ImportError as e:
        print(f"❌ LangChain Anthropic import failed: {e}")
        return False
    
    try:
        from langgraph_supervisor import create_supervisor
        print("✅ LangGraph Supervisor imported successfully")
    except ImportError as e:
        print(f"❌ LangGraph Supervisor import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True


def test_project_imports():
    """Test that project modules can be imported"""
    print("\nTesting project imports...")
    
    try:
        from config import MODEL_NAME, MOCK_DATA_DIR
        print(f"✅ Config imported successfully (Model: {MODEL_NAME})")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from agents import (
            route_planner_agent,
            procurement_manager_agent,
            inventory_manager_agent,
            distribution_handler_agent,
            demand_forecaster_agent,
            cost_optimizer_agent,
        )
        print("✅ All agents imported successfully")
    except ImportError as e:
        print(f"❌ Agent import failed: {e}")
        return False
    
    try:
        from utils import load_scenario, list_available_scenarios
        print("✅ Utils imported successfully")
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    try:
        from main import create_logistics_graph
        print("✅ Main module imported successfully")
    except ImportError as e:
        print(f"❌ Main module import failed: {e}")
        return False
    
    return True


def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    
    from pathlib import Path
    
    required_files = [
        "streamlit_app.py",
        "main.py",
        "requirements.txt",
        "run_streamlit.bat",
        "run_streamlit.sh",
        "STREAMLIT_README.md",
        "STREAMLIT_QUICKSTART.md",
        "UI_FEATURES.md",
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist


def test_scenario_data():
    """Test that scenario data is accessible"""
    print("\nTesting scenario data...")
    
    try:
        from config import MOCK_DATA_DIR
        from pathlib import Path
        
        scenario_index = MOCK_DATA_DIR / "scenario_index.csv"
        
        if scenario_index.exists():
            print(f"✅ Scenario index found at {scenario_index}")
            
            import pandas as pd
            df = pd.read_csv(scenario_index)
            print(f"✅ Found {len(df)} scenarios")
            
            return True
        else:
            print(f"❌ Scenario index not found at {scenario_index}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing scenario data: {e}")
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("STREAMLIT UI SETUP TEST")
    print("="*70 + "\n")
    
    results = []
    
    # Test 1: Imports
    results.append(("External Imports", test_imports()))
    
    # Test 2: Project Imports
    results.append(("Project Imports", test_project_imports()))
    
    # Test 3: File Structure
    results.append(("File Structure", test_file_structure()))
    
    # Test 4: Scenario Data
    results.append(("Scenario Data", test_scenario_data()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 All tests passed! Your Streamlit UI is ready to use.")
        print("\nNext steps:")
        print("1. Ensure ANTHROPIC_API_KEY is set in .env file")
        print("2. Run: streamlit run streamlit_app.py")
        print("3. Or double-click run_streamlit.bat (Windows) / run_streamlit.sh (Linux/Mac)")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Ensure you're in the project root directory")
        print("3. Check that all project files are present")
    
    print()


if __name__ == "__main__":
    main()

