import asyncio
import os
import hashlib

# Playwright usually fails on standard Vercel serverless functions due to size limits
# We wrap it to prevent the whole API from crashing if playwright is missing
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Use /tmp for serverless runtime compatibility
CACHE_DIR = "/tmp/forensic_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

async def capture_source_screenshot(url: str):
    """
    Captures a high-resolution screenshot of a forensic source URL.
    Returns the absolute path to the screenshot image.
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("Playwright not installed. Skipping screenshot.")
        return None

    if not url or url == "N/A":
        return None
        
    url_hash = hashlib.md5(url.encode()).hexdigest()
    filename = f"evidence_{url_hash}.png"
    filepath = os.path.join(CACHE_DIR, filename)
    
    # Return cached version if exists
    if os.path.exists(filepath):
        return os.path.abspath(filepath)
        
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            # Navigate with a generous timeout
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Capture the screenshot
            await page.screenshot(path=filepath, full_page=False)
            await browser.close()
            
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Forensic Capture Error for {url}: {e}")
            return None

async def capture_all_evidence(results: list):
    """
    Captures screenshots for a list of search results in parallel.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return []

    tasks = []
    # Capture only the top 3 high-impact sources
    for r in results[:3]:
        url = r.get('href')
        if url:
            tasks.append(capture_source_screenshot(url))
            
    # Run captures concurrently
    paths = await asyncio.gather(*tasks)
    return [p for p in paths if p]
