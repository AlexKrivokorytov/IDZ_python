"""
Unit tests for Task 3.1 (Resiliency and Error Handling Mocking).
"""

import httpx
import pytest
import respx  # type: ignore[import-not-found]

from security_utils import check_resource


@pytest.mark.asyncio
@respx.mock  # type: ignore[untyped-decorator]
async def test_check_resource_timeout() -> None:
    """
    Test that check_resource correctly raises httpx.RequestError on connection timeout.

    Args: None
    Returns: None
    Raises: None
    """
    url = "https://example.com/api"
    respx.get(url).mock(side_effect=httpx.ConnectTimeout("Connection timed out"))

    async with httpx.AsyncClient() as client:
        with pytest.raises(httpx.RequestError):
            await check_resource(client, "TimeoutResource", url)


@pytest.mark.asyncio
@respx.mock  # type: ignore[untyped-decorator]
async def test_check_resource_503() -> None:
    """
    Test that check_resource does not crash on 503 Service Unavailable.

    Args: None
    Returns: None
    Raises: None
    """
    url = "https://example.com/api"
    respx.get(url).mock(return_value=httpx.Response(503, text="Service Unavailable"))

    async with httpx.AsyncClient() as client:
        result = await check_resource(client, "Resource503", url)
        assert result == "Data from Resource503"


@pytest.mark.asyncio
@respx.mock  # type: ignore[untyped-decorator]
async def test_check_resource_corrupted_data() -> None:
    """
    Test that check_resource does not crash when server returns 200 but invalid JSON/HTML.

    Args: None
    Returns: None
    Raises: None
    """
    url = "https://example.com/api"
    respx.get(url).mock(return_value=httpx.Response(200, text="<!DOCTYPE html><html>"))

    async with httpx.AsyncClient() as client:
        result = await check_resource(client, "CorruptedResource", url)
        assert result == "Data from CorruptedResource"
