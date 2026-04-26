# Contributing

Thanks for taking interest! This is a portfolio project, but suggestions
and pull requests are very welcome.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate     # Linux/macOS
# or  .venv\Scripts\activate    on Windows
pip install -r requirements.txt
pip install pytest pytest-asyncio ruff
```

## Running tests

```bash
pytest tests/test_formatters.py -v
```

## Code style

- `ruff check bot/` must be clean
- Type hints on public functions
- Async I/O via `aiohttp` and `aiosqlite`

## Pull requests

- Keep PRs focused on a single concern
- Add or update tests when changing behaviour
- Update README if you add a new bot command
