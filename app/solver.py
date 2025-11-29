import json
import asyncio
import httpx
import hashlib
from app.scraper import extract_task_from_page
from app.utils import compute_answer


# -----------------------------
# DEMO2: Alphametic solver
# -----------------------------
def solve_demo2(email: str):
    """Solve Demo2 alphametic puzzle drawn on canvas."""
    # 1. First 4 hex of SHA1(email)
    sha = hashlib.sha1(email.encode()).hexdigest()
    first4 = sha[:4]
    email_number = int(first4, 16)

    # 2. Formula:
    # key = ((emailNumber * 7919 + 12345) mod 1e8)
    key_val = (email_number * 7919 + 12345) % 100000000
    key_str = f"{key_val:08d}"  # ensure 8 digits

    F, O, R, K, L, I, M, E = map(int, key_str)

    left = int(f"{F}{O}{R}{K}")
    right = int(f"{L}{I}{M}{E}")
    return left + right


async def solve_quiz_task(email: str, secret: str, first_url: str):
    current_url = first_url
    final_answer = None

    async with httpx.AsyncClient(timeout=90) as client:
        while current_url is not None:

            # 1. Load quiz page
            task_data = await extract_task_from_page(current_url)
            raw = task_data.raw_html

            # ----------------------------------------------------------
            # Detect DEMO2 alphametic puzzle (canvas + script pattern)
            # ----------------------------------------------------------
            if "<canvas id=\"puzzle\"" in raw or "ALPHAMETIC" in raw:
                print("\n🧩 Detected DEMO2 Alphametic Puzzle!")
                answer = solve_demo2(email)
            else:
                # normal quiz question
                answer = await compute_answer(task_data)

            # 3. Submit answer
            payload = {
                "email": email,
                "secret": secret,
                "url": current_url,
                "answer": answer
            }

            print("\n--- SUBMIT URL DETECTED ---")
            print(task_data.submit_url)
            print("---------------------------\n")

            resp = await client.post(task_data.submit_url, json=payload)
            out = resp.json()

            # Retrying logic (allowed within 3 minutes)
            if not out.get("correct"):
                last_try = await client.post(task_data.submit_url, json=payload)
                out = last_try.json()

            # Move to next URL if present
            current_url = out.get("url")
            final_answer = answer

        return final_answer
