import sys
import asyncio

# Fix Playwright on Windows
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception as e:
        print("Failed to set Windows event loop:", e)
