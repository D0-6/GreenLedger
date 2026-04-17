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

# Use forensic_cache relative to the api directory for consistency
CACHE_DIR = os.path.join(os.path.dirname(__file__), "forensic_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

async def capture_source_screenshot(url: str, browser=None):
    """
    Captures a high-resolution screenshot of a forensic source URL.
    If browser is provided, uses it for faster parallel capture.
    """
    if not PLAYWRIGHT_AVAILABLE and not browser:
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
        
    if browser:
        try:
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
            await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await asyncio.sleep(2)
            await page.screenshot(path=filepath, full_page=False)
            await page.close()
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Parallel Capture Error for {url}: {e}")
            return None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await asyncio.sleep(2)
            await page.screenshot(path=filepath, full_page=False)
            await browser.close()
            return os.path.abspath(filepath)
        except Exception as e:
            print(f"Standalone Capture Error for {url}: {e}")
            return None

async def capture_all_evidence(results: list):
    """
    Captures screenshots for a list of search results in parallel using one browser.
    """
    if not PLAYWRIGHT_AVAILABLE or not results:
        return []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = []
        # Support up to 8 parallel sources for Institutional Audit
        for r in results[:8]:
            url = r.get('href')
            if url:
                tasks.append(capture_source_screenshot(url, browser=browser))
        
        # Run captures concurrently in separate tabs
        paths = await asyncio.gather(*tasks)
        await browser.close()
        return [p for p in paths if p]
