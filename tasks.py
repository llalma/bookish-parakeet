from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import uuid
import os

import sys
sys.setrecursionlimit(20000)


TIME_LIMIT = 100 # Seconbds

celery_app = Celery('tasks')

def calc_fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using a recursive approach.

    Args:
        n (int): The position in the Fibonacci sequence to calculate.

    Returns:
        int: The Fibonacci number at position n.
    """
    if n <= 1:
        return n
    return calc_fib(n - 1) + calc_fib(n - 2)

@celery_app.task(soft_time_limit=TIME_LIMIT)
def process_task(inputs: dict):
    """
    A Celery task that computes a Fibonacci number and returns a structured report.
    Args:
        inputs (dict): Input dictionary for celery task

    Returns:
        dict: A dictionary containing:
            - status (str): The completion status ("DONE").
            - input_number (int): The original input provided.
            - result (int): The calculated Fibonacci number.
            - id (uuid.UUID): A unique identifier for this specific process run.
    """
    target_number = inputs['target']
    try:
        res = calc_fib(target_number)
        return {
                "status": "DONE", 
                "input_number": target_number, 
                "result": res,
                "id": uuid.uuid4()
                }
    except SoftTimeLimitExceeded:
        return {
            "status": "ERROR",
            "input_number": target_number,
            "result": None,
            "error": f"Task took longer than {TIME_LIMIT} seconds and was aborted.",
            "id": str(uuid.uuid4())
        }

if __name__ == "__main__":
    print(calc_fib(6))
