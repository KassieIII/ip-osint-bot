# 🔍 IP OSINT Telegram Bot

A Telegram bot for quick IP address and domain intelligence gathering. Returns geolocation, ISP info, DNS records, and WHOIS data in a clean formatted message.

## Features

- **IP Geolocation** — Country, city, coordinates, timezone
- **ISP & ASN Info** — Provider, organization, autonomous system
- **DNS Lookup** — A, AAAA, MX, NS, TXT records
- **WHOIS Data** — Registrar, creation date, expiration
- **Bulk Lookup** — Process multiple IPs/domains at once
- **Rate Limiting** — Prevents abuse with per-user cooldowns
- **History** — Stores last 10 lookups per user

## Tech Stack

- Python 3.11+
- python-telegram-bot (async)
- aiohttp for non-blocking API calls
- SQLite for user history
- ip-api.com + ipwhois for data sources

## Quick Start

```bash
# Clone
git clone https://github.com/KassieIII/ip-osint-bot.git
cd ip-osint-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Telegram bot token

# Run
python -m bot.main
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram Bot API token from @BotFather |
| `RATE_LIMIT` | Max requests per minute per user (default: 10) |
| `DB_PATH` | SQLite database path (default: `data/history.db`) |

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and usage info |
| `/ip <address>` | Lookup IP address |
| `/domain <name>` | Lookup domain (DNS + WHOIS) |
| `/bulk <ip1> <ip2> ...` | Bulk IP lookup (max 5) |
| `/history` | Show your last 10 lookups |
| `/help` | List all commands |

## Project Structure

```
ip-osint-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py          # Entry point, bot setup
│   ├── handlers.py      # Command handlers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ip_lookup.py     # IP geolocation service
│   │   ├── dns_lookup.py    # DNS resolution service
│   │   └── whois_lookup.py  # WHOIS query service
│   ├── database.py      # SQLite history storage
│   ├── rate_limiter.py  # Per-user rate limiting
│   └── formatters.py    # Message formatting utilities
├── tests/
│   ├── test_ip_lookup.py
│   ├── test_dns_lookup.py
│   └── test_formatters.py
├── .env.example
├── requirements.txt
└── README.md
```

## License

MIT
