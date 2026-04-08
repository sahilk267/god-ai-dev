import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

async def demo_training():
    print("--- 🧠 God-Level AI: Memory Training Demo ---")
    
    url = "https://chatgpt.com/share/69d6d898-2cc4-83a3-b7f1-d74aae387c5a"
    print(f"🔗 Target: {url}")
    
    try:
        from backend.services.scraper_service import scraper_service
        from backend.agents.master import master_agent
        
        print("📥 Scraping and extracting knowledge...")
        content = await scraper_service.extract_text_from_url(url)
        
        if content:
            print(f"✅ Extracted {len(content)} characters of conversation.")
            print("💾 Training Master Agent...")
            num_patterns = await master_agent.extract_knowledge_from_logs(content)
            print(f"✨ Success! Extracted {num_patterns} patterns into permanent memory.")
            
            print("\n🔍 Verifying Memory (Testing Retrieval)...")
            advice = await master_agent.get_advice("build a resume builder app")
            print("ADVICE FROM YOUR CHATS:")
            print(advice[:500] + "...")
        else:
            print("❌ Failed to extract content from URL. Make sure it is public.")
            
    except Exception as e:
        print(f"❌ Demo runtime error: {e}")

if __name__ == "__main__":
    asyncio.run(demo_training())
