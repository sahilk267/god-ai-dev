import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

async def test_learning():
    print("--- Verifying System Components ---")
    
    try:
        import chromadb
        print("[SUCCESS] chromadb is installed")
    except ImportError:
        print("[ERROR] chromadb is NOT installed. Please run: pip install -r requirements.txt")
        return

    try:
        from backend.agents.master import master_agent
        from backend.core.experience import experience_service
        print("[SUCCESS] Master Agent and Experience Service loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load agents: {e}")
        return

    print("\n--- Running Mock Training Session ---")
    sample_logs = """
    User: I prefer using FastAPI with Pydantic V2.
    Assistant: Noted. Use BaseSettings from pydantic-settings for configuration.
    User: How about database?
    Assistant: Use SQLAlchemy for Postgres, and always implement an AsyncSession.
    """
    
    try:
        count = await master_agent.extract_knowledge_from_logs(sample_logs)
        print(f"[SUCCESS] Extracted {count} patterns!")
        
        print("\n--- Querying memory for 'Setup Postgres' ---")
        advice = await master_agent.get_advice("setup postgres database connection")
        print(f"ADVICE RECEIVED:\n{advice}")
        
        if "PATTERN:" in advice or "LESSON:" in advice:
            print("\n[COMPLETE] SYSTEM VERIFIED: Learning and Retrieval is operational!")
        else:
            print("\n[PARTIAL] SYSTEM PARTIAL: Vector search returned no results. Check model outputs.")
            
    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_learning())
