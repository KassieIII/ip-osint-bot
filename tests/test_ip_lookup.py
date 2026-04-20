import pytest
from unittest.mock import patch, AsyncMock
from bot.services.ip_lookup import lookup_ip


@pytest.mark.asyncio
async def test_lookup_ip_success():
    mock_response = {
        "status": "success",
        "query": "8.8.8.8",
        "country": "United States",
        "countryCode": "US",
        "regionName": "Virginia",
        "city": "Ashburn",
        "zip": "20149",
        "lat": 39.03,
        "lon": -77.5,
        "timezone": "America/New_York",
        "isp": "Google LLC",
        "org": "Google Public DNS",
        "as": "AS15169 Google LLC",
    }

    with patch("bot.services.ip_lookup.aiohttp.ClientSession") as mock_session:
        mock_resp = AsyncMock()
        mock_resp.json = AsyncMock(return_value=mock_response)
        mock_ctx = AsyncMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        mock_session_inst = AsyncMock()
        mock_session_inst.get = lambda *a, **kw: mock_ctx
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session_inst)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await lookup_ip("8.8.8.8")
        assert result["ip"] == "8.8.8.8"
        assert result["country"] == "United States"
        assert result["isp"] == "Google LLC"


@pytest.mark.asyncio
async def test_lookup_ip_fail():
    mock_response = {"status": "fail", "message": "invalid query"}

    with patch("bot.services.ip_lookup.aiohttp.ClientSession") as mock_session:
        mock_resp = AsyncMock()
        mock_resp.json = AsyncMock(return_value=mock_response)
        mock_ctx = AsyncMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        mock_session_inst = AsyncMock()
        mock_session_inst.get = lambda *a, **kw: mock_ctx
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session_inst)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)

        with pytest.raises(ValueError, match="invalid query"):
            await lookup_ip("invalid")
