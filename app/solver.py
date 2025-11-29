import json
import asyncio
import httpx
from app.scraper import extract_task_from_page
from app.utils import compute_answer


async def solve_quiz_task(email: str, secret: str, first_url: str):
    current_url = first_url
    final_answer = None

    async with httpx.AsyncClient(timeout=90) as client:
        while current_url is not None:
            # 1. Load quiz page and extract the question
            task_data = await extract_task_from_page(current_url)

            # 2. Solve the task (logic may include scraping, PDF, math, LLM)
            answer = await compute_answer(task_data)

            # 3. Submit the answer to the server
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

            if not out.get("correct"):
                # Retry is allowed within 3 minutes
                last_try = await client.post(task_data.submit_url, json=payload)
                out = last_try.json()

            current_url = out.get("url")  # next quiz URL
            final_answer = answer

        return final_answer
