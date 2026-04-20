import asyncio
import whois


async def lookup_whois(domain: str) -> dict:
    """Fetch WHOIS data for a domain."""
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, whois.whois, domain)
    except Exception:
        return {"domain": domain, "error": "WHOIS lookup failed"}

    def _extract_date(value):
        if isinstance(value, list):
            value = value[0]
        return str(value) if value else "N/A"

    return {
        "domain": domain,
        "registrar": data.get("registrar", "N/A") or "N/A",
        "creation_date": _extract_date(data.get("creation_date")),
        "expiration_date": _extract_date(data.get("expiration_date")),
        "name_servers": data.get("name_servers", []) or [],
        "status": data.get("status", "N/A") or "N/A",
    }
