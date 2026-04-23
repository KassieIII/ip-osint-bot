import asyncio
import ipaddress
from typing import AsyncIterator


async def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a TCP port is open on a host."""
    try:
        fut = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False


async def scan_host(host: str, ports: list[int]) -> dict:
    """Scan multiple ports on a single host concurrently."""
    tasks = [scan_port(host, p) for p in ports]
    results = await asyncio.gather(*tasks)
    return {
        "host": host,
        "open_ports": [p for p, is_open in zip(ports, results) if is_open],
    }


async def scan_subnet(
    cidr: str, ports: list[int], max_hosts: int = 32
) -> AsyncIterator[dict]:
    """Scan a CIDR subnet for hosts with open ports."""
    network = ipaddress.ip_network(cidr, strict=False)

    if network.num_addresses > max_hosts:
        raise ValueError(
            f"Subnet too large: {network.num_addresses} hosts (max {max_hosts})"
        )

    semaphore = asyncio.Semaphore(10)

    async def scan_with_limit(host: str) -> dict:
        async with semaphore:
            return await scan_host(host, ports)

    tasks = [scan_with_limit(str(ip)) for ip in network.hosts()]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result["open_ports"]:
            yield result


COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
