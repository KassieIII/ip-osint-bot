def format_ip_result(data: dict) -> str:
    """Format IP lookup result as a Telegram message."""
    flag = _country_flag(data.get("country_code", ""))

    lines = [
        f"📍 <b>IP: {data['ip']}</b>",
        "",
        f"{flag} <b>Location</b>",
        f"  Country: {data['country']}",
        f"  Region: {data['region']}",
        f"  City: {data['city']}",
        f"  ZIP: {data['zip']}",
        f"  Coords: {data['lat']}, {data['lon']}",
        f"  Timezone: {data['timezone']}",
        "",
        "🏢 <b>Network</b>",
        f"  ISP: {data['isp']}",
        f"  Org: {data['org']}",
        f"  ASN: {data['asn']}",
    ]
    return "\n".join(lines)


def format_dns_result(data: dict) -> str:
    """Format DNS lookup result."""
    records = data.get("records", {})
    lines = ["📡 <b>DNS Records</b>"]

    for rtype, values in records.items():
        if values:
            formatted = ", ".join(values[:5])
            lines.append(f"  {rtype}: <code>{formatted}</code>")
        else:
            lines.append(f"  {rtype}: —")

    return "\n".join(lines)


def format_whois_result(data: dict) -> str:
    """Format WHOIS lookup result."""
    if "error" in data:
        return "📄 <b>WHOIS:</b> Data unavailable"

    ns_list = data.get("name_servers", [])
    ns_text = ", ".join(ns_list[:4]) if ns_list else "N/A"

    lines = [
        "📄 <b>WHOIS</b>",
        f"  Registrar: {data.get('registrar', 'N/A')}",
        f"  Created: {data.get('creation_date', 'N/A')}",
        f"  Expires: {data.get('expiration_date', 'N/A')}",
        f"  NS: <code>{ns_text}</code>",
    ]
    return "\n".join(lines)


def _country_flag(code: str) -> str:
    """Convert country code to flag emoji."""
    if not code or len(code) != 2:
        return "🌍"
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code.upper())
