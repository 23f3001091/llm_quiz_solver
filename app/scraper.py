import asyncio
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
import re

class QuizTask:
    def __init__(self, question, submit_url, raw_html):
        self.question = question
        self.submit_url = submit_url
        self.raw_html = raw_html


def clean_url(url: str):
    """Remove HTML garbage from extracted URL."""
    if not url:
        return None

    # Remove HTML tags and broken characters
    url = url.replace("</span>", "")
    url = url.replace("</p>", "")
    url = url.replace("</div>", "")
    url = url.replace(">", "")
    url = url.replace("\"", "")
    url = url.replace("'", "")
    url = url.strip()

    return url


def load_page_sync(url: str):
    """Runs Playwright sync mode in a thread (Windows-safe)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        html = page.content()
        text = page.inner_text("body")

        # ----------------------------------------------
        # STRONG & CLEAN SUBMIT URL EXTRACTION (3 levels)
        # ----------------------------------------------

        # ----------------------------------------------
        # STRONG & CLEAN SUBMIT URL EXTRACTION (supports relative links)
        # ----------------------------------------------

        submit_url = None

        # Base domain (for resolving relative URLs)
        from urllib.parse import urljoin

        base_url = url.split("?")[0]  # strip query
        base_origin = re.match(r"https?://[^/]+", url).group(0)

        # 1) Look for absolute URLs
        abs_urls = re.findall(r"https?://[^\s\"'>]+", html)

        for u in abs_urls:
            if "submit" in u:
                submit_url = clean_url(u)
                break

        # 2) Look for relative URLs like /submit
        if submit_url is None:
            rel_candidates = re.findall(r"href=['\"](/submit[^'\">]*)['\"]", html)
            if rel_candidates:
                submit_url = urljoin(base_origin, rel_candidates[0])

        # 3) Fallback: URLs inside visible text
        if submit_url is None:
            visible_urls = re.findall(r"https?://[^\s\"'>]+", text)
            for u in visible_urls:
                if "submit" in u:
                    submit_url = clean_url(u)
                    break

        # Clean again
        if submit_url:
            submit_url = clean_url(submit_url)

        if submit_url is None:
            print("\n❌ Could not find submit URL in page\n")
            print("HTML snippet:")
            print(html[:1500])
            raise ValueError("Submit URL not found")

        browser.close()

        return QuizTask(question=text, submit_url=submit_url, raw_html=html)


async def extract_task_from_page(url: str) -> QuizTask:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, load_page_sync, url)
