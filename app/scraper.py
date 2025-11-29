import asyncio
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
import re
from urllib.parse import urlparse, urljoin

class QuizTask:
    def __init__(self, question, submit_url, raw_html):
        self.question = question
        self.submit_url = submit_url
        self.raw_html = raw_html


def clean_url(url: str):
    if not url:
        return None
    return (
        url.replace("</span>", "")
           .replace("</p>", "")
           .replace("</div>", "")
           .replace(">", "")
           .replace("\"", "")
           .replace("'", "")
           .strip()
    )


def load_page_sync(url: str):
    """Runs Playwright sync mode in a thread (Windows-safe)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        html = page.content()
        text = page.inner_text("body")

        submit_url = None
        parsed = urlparse(url)
        base_origin = f"{parsed.scheme}://{parsed.netloc}"

        # ------------------------------------------------------
        # 1) Look for absolute submit URLs
        # ------------------------------------------------------
        abs_urls = re.findall(r"https?://[^\s\"'>]+", html)
        for u in abs_urls:
            if "submit" in u:
                submit_url = clean_url(u)
                break

        # ------------------------------------------------------
        # 2) Look for relative URLs such as /submit or /submit?...
        # ------------------------------------------------------
        if submit_url is None:
            rel_urls = re.findall(r"href=['\"](/submit[^'\">]*)['\"]", html)
            if rel_urls:
                submit_url = urljoin(base_origin, rel_urls[0])

        # ------------------------------------------------------
        # 3) Fallback: look in visible text
        # ------------------------------------------------------
        if submit_url is None:
            visible_urls = re.findall(r"https?://[^\s\"'>]+", text)
            for u in visible_urls:
                if "submit" in u:
                    submit_url = clean_url(u)
                    break

        # ------------------------------------------------------
        # 4) FINAL FALLBACK (needed for Demo2)
        # There is NO submit URL in Demo2, so we infer it.
        # ------------------------------------------------------
        if submit_url is None:
            submit_url = f"{base_origin}/submit"
            print("\n⚠️ Fallback: Using inferred submit URL:", submit_url)

        browser.close()
        return QuizTask(question=text, submit_url=submit_url, raw_html=html)


async def extract_task_from_page(url: str) -> QuizTask:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, load_page_sync, url)
