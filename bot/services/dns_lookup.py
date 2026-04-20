import asyncio
import dns.resolver


RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT"]


async def lookup_dns(domain: str) -> dict:
    """Resolve DNS records for a domain."""
    loop = asyncio.get_event_loop()
    results = {}

    for rtype in RECORD_TYPES:
        try:
            answer = await loop.run_in_executor(
                None, _resolve_sync, domain, rtype
            )
            results[rtype] = answer
        except Exception:
            results[rtype] = []

    return {"domain": domain, "records": results}


def _resolve_sync(domain: str, rtype: str) -> list[str]:
    """Synchronous DNS resolution (run in executor)."""
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        answers = resolver.resolve(domain, rtype)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return []
