"""
Security utilities and asynchronous systems module for testing laboratory work.
"""

import asyncio
import os
import random
from typing import Dict, List, Optional

import httpx


# Task 1.1: Password Validation
def validate_password(password: str) -> bool:
    """
    Validates a password based on length, digit inclusion, and forbidden words.

    Args:
        password: The password string to validate.

    Returns:
        True if the password meets all criteria, False otherwise.

    Raises: None
    """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if "admin" in password.lower():
        return False
    return True


# Task 2.1 & 2.2: Async Search Agent with Interruption (from lab6source.py)
async def recursive_search(
    path: str, extension: str, stop_event: asyncio.Event, results: List[str]
) -> None:
    """
    Recursively searches for files with a specific extension, supporting interruption.

    Args:
        path: The directory path to start the search.
        extension: The file extension to look for.
        stop_event: Event to signal search termination.
        results: List to store found file paths.

    Returns: None
    Raises: None
    """
    print(f"[Search] Scanning started: {path}")
    for root, dirs, files in os.walk(path):
        if stop_event.is_set():
            print("[Search] Stop signal received. Aborting...")
            break
        for file in files:
            if file.endswith(extension):
                results.append(os.path.join(root, file))
        await asyncio.sleep(0)


# Task 3.1: Resource Checker (from lab6source.py Task 1.1)
async def check_resource(client: httpx.AsyncClient, name: str, url: str) -> str:
    """
    Checks resource availability with an HTTP GET request.

    Args:
        client: The async HTTP client.
        name: The name of the resource.
        url: The URL to check.

    Returns:
        A string indicating the data source.

    Raises:
        httpx.RequestError: If a network error or timeout occurs.
    """
    print(f"--- Resource {name} check started ---")
    response = await client.get(url)
    print(f"--- Resource {name} checked (Status: {response.status_code}) ---")
    return f"Data from {name}"


# Task 3.2: Race Conditions & Atomic Updates
class ResourceCounter:
    """
    A counter resource demonstrating race conditions and atomic updates using asyncio.Lock.
    """

    def __init__(self) -> None:
        """Initializes the counter and its lock."""
        self.count: int = 0
        self.lock: asyncio.Lock = asyncio.Lock()

    async def increment(self) -> None:
        """
        Increments the counter with an intentional race condition.

        Args: None
        Returns: None
        Raises: None
        """
        current = self.count
        await asyncio.sleep(0)
        self.count = current + 1

    async def increment_locked(self) -> None:
        """
        Increments the counter atomically using an asyncio.Lock.

        Args: None
        Returns: None
        Raises: None
        """
        async with self.lock:
            current = self.count
            await asyncio.sleep(0)
            self.count = current + 1


# Task 3.3: Producer-Consumer Queue (from lab6source.py Task 3.1)
async def producer(queue: asyncio.Queue[Optional[str]], count: int) -> None:
    """
    Generates messages and places them into an async queue.

    Args:
        queue: The async queue for messages.
        count: The number of messages to generate.

    Returns: None
    Raises: None
    """
    for i in range(1, count + 1):
        msg = f"Log message #{i}"
        await queue.put(msg)
        await asyncio.sleep(random.uniform(0.01, 0.03))
    await queue.put(None)
    await queue.put(None)
    print("[Producer] Work finished, markers placed.")


async def consumer(
    name: str, queue: asyncio.Queue[Optional[str]], stats: Dict[str, int]
) -> None:
    """
    Processes messages from the queue.

    Args:
        name: The name of the consumer.
        queue: The async queue to read from.
        stats: Dictionary to track processing statistics.

    Returns: None
    Raises: None
    """
    while True:
        msg = await queue.get()
        if msg is None:
            queue.task_done()
            print(f"[Consumer {name}] Termination signal received.")
            break
        await asyncio.sleep(0.01)
        stats[name] += 1
        queue.task_done()
        print(f"[Consumer {name}] Processed: {msg}")
