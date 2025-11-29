import re
import random

async def compute_answer(task):
    """
    Dummy universal solver.
    You can enhance it with LLM calls when needed.
    """
    text = task.question.lower()

    # Example numeric extraction
    nums = re.findall(r"\d+", text)
    if nums:
        return sum(int(n) for n in nums)

    # Fallback: return a random but valid string
    return "processed"
