import pytest
from bot.services.dns_lookup import _resolve_sync


class TestResolveSyncIntegration:
    """Basic tests for DNS resolution (requires network)."""

    def test_resolve_a_record(self):
        result = _resolve_sync("google.com", "A")
        assert len(result) > 0
        assert all("." in r for r in result)

    def test_resolve_nonexistent(self):
        result = _resolve_sync("this-domain-does-not-exist-12345.com", "A")
        assert result == []

    def test_resolve_mx(self):
        result = _resolve_sync("google.com", "MX")
        assert len(result) > 0
