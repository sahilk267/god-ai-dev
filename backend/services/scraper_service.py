import trafilatura
import httpx
from backend.core.logger import get_logger
from typing import Optional

logger = get_logger(__name__)

class ScraperService:
    async def extract_text_from_url(self, url: str) -> Optional[str]:
        """Fetch a URL and extract its main text content"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                html_content = response.text
                
            # Use trafilatura for high-quality text extraction
            text = trafilatura.extract(html_content, include_comments=False, include_tables=True)
            
            if not text and "chatgpt.com/share" in url:
                # Fallback for ChatGPT share links if trafilatura fails
                # They often embed data in a JSON script tag
                import re
                import json
                match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_content)
                if match:
                    data = json.loads(match.group(1))
                    # Extract conversations from the JSON structure
                    # This structure changes occasionally, so we try a general extraction
                    conversations = data.get("props", {}).get("pageProps", {}).get("serverResponse", {}).get("data", {}).get("content", [])
                    if conversations:
                        text = "\n\n".join([f"{c['role'].upper()}: {c['content']['parts'][0]}" for c in conversations if 'parts' in c.get('content', {})])

            if text:
                logger.info(f"Successfully extracted {len(text)} characters from {url}")
                return text
            
            logger.warning(f"No text extracted from {url}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return None

scraper_service = ScraperService()
