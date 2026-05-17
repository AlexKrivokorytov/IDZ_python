"""
Unit tests for Task 2.2 (Interruption Mechanisms and Signals).
"""

import asyncio
import pathlib

import pytest

from security_utils import recursive_search


@pytest.mark.asyncio
async def test_recursive_search_stop_event(tmp_path: pathlib.Path) -> None:
    """
    Test that recursive_search aborts immediately if stop_event is set before scanning.

    Args:
        tmp_path: Temporary directory fixture provided by pytest.

    Returns: None
    Raises: None
    """
    for i in range(15):
        (tmp_path / f"file_{i}.log").write_text("content")

    stop_event = asyncio.Event()
    stop_event.set()

    results: list[str] = []
    await recursive_search(str(tmp_path), ".log", stop_event, results)

    assert len(results) == 0
