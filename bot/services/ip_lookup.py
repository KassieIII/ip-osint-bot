import aiohttp

IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"


async def lookup_ip(ip: str) -> dict:
    """Query ip-api.com for geolocation and ISP data."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            IP_API_URL.format(ip=ip),
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            data = await resp.json()

    if data.get("status") == "fail":
        raise ValueError(f"API error: {data.get('message', 'Unknown error')}")

    return {
        "ip": data.get("query", ip),
        "country": data.get("country", "N/A"),
        "country_code": data.get("countryCode", ""),
        "region": data.get("regionName", "N/A"),
        "city": data.get("city", "N/A"),
        "zip": data.get("zip", "N/A"),
        "lat": data.get("lat", 0),
        "lon": data.get("lon", 0),
        "timezone": data.get("timezone", "N/A"),
        "isp": data.get("isp", "N/A"),
        "org": data.get("org", "N/A"),
        "asn": data.get("as", "N/A"),
    }
