"""
Unit tests for Task 2.1 (Asynchronous Search Agent).
"""

import asyncio
import pathlib

import pytest

from security_utils import recursive_search


@pytest.mark.asyncio
async def test_recursive_search_success(tmp_path: pathlib.Path) -> None:
    """
    Test that recursive_search correctly finds files by extension in a directory structure.

    Args:
        tmp_path: Temporary directory fixture provided by pytest.

    Returns: None
    Raises: None
    """
    sub1 = tmp_path / "sub1"
    sub2 = tmp_path / "sub2"
    sub1.mkdir()
    sub2.mkdir()

    (tmp_path / "test1.log").write_text("log content")
    (sub1 / "test2.log").write_text("log content")
    (sub1 / "ignore.txt").write_text("text content")
    (sub2 / "test3.log").write_text("log content")

    stop_event = asyncio.Event()
    results: list[str] = []

    await recursive_search(str(tmp_path), ".log", stop_event, results)

    assert len(results) == 3
    assert any("test1.log" in p for p in results)
    assert any("test2.log" in p for p in results)
    assert any("test3.log" in p for p in results)
