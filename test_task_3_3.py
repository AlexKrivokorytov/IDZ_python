"""
Unit tests for Task 3.3 (Producer-Consumer Queue).
"""

import asyncio
from typing import Optional

import pytest

from security_utils import consumer, producer


@pytest.mark.asyncio
async def test_producer_consumer_queue() -> None:
    """
    Test verifying that consumer processes exactly 10 messages before terminating on None marker.

    Args: None
    Returns: None
    Raises: None
    """
    queue: asyncio.Queue[Optional[str]] = asyncio.Queue()
    stats = {"C1": 0}

    await producer(queue, 10)

    consumer_task = asyncio.create_task(consumer("C1", queue, stats))
    await consumer_task

    assert stats["C1"] == 10
