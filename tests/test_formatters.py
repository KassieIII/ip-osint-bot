import pytest
from bot.formatters import format_ip_result, format_dns_result, format_whois_result, _country_flag


class TestFormatIpResult:
    def test_basic_format(self):
        data = {
            "ip": "8.8.8.8",
            "country": "United States",
            "country_code": "US",
            "region": "Virginia",
            "city": "Ashburn",
            "zip": "20149",
            "lat": 39.03,
            "lon": -77.5,
            "timezone": "America/New_York",
            "isp": "Google LLC",
            "org": "Google Public DNS",
            "asn": "AS15169 Google LLC",
        }
        result = format_ip_result(data)
        assert "8.8.8.8" in result
        assert "United States" in result
        assert "Google LLC" in result

    def test_missing_country_code(self):
        data = {
            "ip": "1.1.1.1",
            "country": "Australia",
            "country_code": "",
            "region": "NSW",
            "city": "Sydney",
            "zip": "2000",
            "lat": -33.8,
            "lon": 151.2,
            "timezone": "Australia/Sydney",
            "isp": "Cloudflare",
            "org": "Cloudflare",
            "asn": "AS13335",
        }
        result = format_ip_result(data)
        assert "🌍" in result


class TestFormatDnsResult:
    def test_with_records(self):
        data = {
            "domain": "example.com",
            "records": {
                "A": ["93.184.216.34"],
                "AAAA": [],
                "MX": ["mail.example.com"],
                "NS": ["ns1.example.com", "ns2.example.com"],
                "TXT": [],
            },
        }
        result = format_dns_result(data)
        assert "93.184.216.34" in result
        assert "A:" in result
        assert "—" in result  # empty AAAA

    def test_empty_records(self):
        data = {"domain": "test.com", "records": {}}
        result = format_dns_result(data)
        assert "DNS Records" in result


class TestFormatWhoisResult:
    def test_with_data(self):
        data = {
            "domain": "example.com",
            "registrar": "ICANN",
            "creation_date": "1995-08-14",
            "expiration_date": "2026-08-13",
            "name_servers": ["ns1.example.com"],
            "status": "active",
        }
        result = format_whois_result(data)
        assert "ICANN" in result
        assert "1995" in result

    def test_with_error(self):
        data = {"domain": "fail.com", "error": "WHOIS lookup failed"}
        result = format_whois_result(data)
        assert "unavailable" in result.lower()


class TestCountryFlag:
    def test_us(self):
        assert _country_flag("US") == "🇺🇸"

    def test_empty(self):
        assert _country_flag("") == "🌍"

    def test_invalid(self):
        assert _country_flag("XYZ") == "🌍"
