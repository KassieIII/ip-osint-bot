# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- `pyproject.toml` with `pytest pythonpath` so test discovery works on CI runners.

### Fixed
- Ruff F541 (unnecessary f-string) in `bot/formatters.py`.
- Ruff F401 (unused import) in `bot/main.py`.

## [0.2.0] - 2026-04-23

### Added
- `/subnet` command for CIDR-range port scanning.
- Async port scanner service using `asyncio.open_connection`.
- GitHub Actions CI (ruff lint + pytest matrix on Python 3.11/3.12).
- Multi-stage Dockerfile for containerised deployment.

## [0.1.0] - 2026-04-20

### Added
- Initial release with `/ip`, `/dns`, `/whois` commands.
- Telegram inline-keyboard navigation.
- WHOIS, RDAP and reverse-DNS formatters.
