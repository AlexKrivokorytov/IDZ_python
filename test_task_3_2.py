"""
Unit tests for Task 3.2 (Race Conditions and Atomic Updates).
"""

import asyncio

import pytest

from security_utils import ResourceCounter


@pytest.mark.asyncio
async def test_resource_counter_race_condition() -> None:
    """
    Test demonstrating that racy increment leads to lost updates (count < 1000).

    Args: None
    Returns: None
    Raises: None
    """
    counter = ResourceCounter()

    async def worker() -> None:
        for _ in range(10):
            await counter.increment()

    workers = [worker() for _ in range(100)]
    await asyncio.gather(*workers)

    assert counter.count < 1000


@pytest.mark.asyncio
async def test_resource_counter_locked() -> None:
    """
    Test demonstrating that locked increment correctly synchronizes updates (count == 1000).

    Args: None
    Returns: None
    Raises: None
    """
    counter = ResourceCounter()

    async def worker() -> None:
        for _ in range(10):
            await counter.increment_locked()

    workers = [worker() for _ in range(100)]
    await asyncio.gather(*workers)

    assert counter.count == 1000
