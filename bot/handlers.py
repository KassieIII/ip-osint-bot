import os
import logging
import ipaddress
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.ip_lookup import lookup_ip
from bot.services.dns_lookup import lookup_dns
from bot.services.whois_lookup import lookup_whois
from bot.formatters import format_ip_result, format_dns_result, format_whois_result
from bot.rate_limiter import RateLimiter
from bot.database import Database

logger = logging.getLogger(__name__)

rate_limiter = RateLimiter(max_requests=int(os.getenv("RATE_LIMIT", "10")))

WELCOME_TEXT = (
    "🔍 <b>IP OSINT Bot</b>\n\n"
    "Gather intelligence on IP addresses and domains.\n\n"
    "<b>Commands:</b>\n"
    "/ip &lt;address&gt; — Lookup IP address\n"
    "/domain &lt;name&gt; — DNS + WHOIS lookup\n"
    "/bulk &lt;ip1&gt; &lt;ip2&gt; ... — Bulk IP lookup (max 5)\n"
    "/history — Your last 10 lookups\n"
    "/help — Show this message"
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT, parse_mode="HTML")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT, parse_mode="HTML")


def _validate_ip(address: str) -> bool:
    try:
        ip = ipaddress.ip_address(address)
        return not ip.is_private and not ip.is_loopback
    except ValueError:
        return False


async def ip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not rate_limiter.is_allowed(user_id):
        await update.message.reply_text("⏳ Rate limit exceeded. Please wait a moment.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /ip <address>\nExample: /ip 8.8.8.8")
        return

    target = context.args[0].strip()

    if not _validate_ip(target):
        await update.message.reply_text("❌ Invalid or private IP address.")
        return

    await update.message.reply_text("🔄 Looking up...")

    try:
        result = await lookup_ip(target)
        text = format_ip_result(result)

        db_path = context.bot_data.get("db_path", "data/history.db")
        async with Database(db_path) as db:
            await db.save_lookup(user_id, "ip", target, result.get("country", ""))

        await update.message.reply_text(text, parse_mode="HTML")
    except Exception as e:
        logger.error("IP lookup failed for %s: %s", target, e)
        await update.message.reply_text("❌ Lookup failed. Please try again later.")


async def domain_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not rate_limiter.is_allowed(user_id):
        await update.message.reply_text("⏳ Rate limit exceeded. Please wait a moment.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /domain <name>\nExample: /domain example.com")
        return

    target = context.args[0].strip().lower()

    if not target or len(target) > 253 or "." not in target:
        await update.message.reply_text("❌ Invalid domain name.")
        return

    await update.message.reply_text("🔄 Resolving...")

    try:
        dns_result = await lookup_dns(target)
        whois_result = await lookup_whois(target)

        dns_text = format_dns_result(dns_result)
        whois_text = format_whois_result(whois_result)

        text = f"🌐 <b>{target}</b>\n\n{dns_text}\n\n{whois_text}"

        db_path = context.bot_data.get("db_path", "data/history.db")
        async with Database(db_path) as db:
            await db.save_lookup(user_id, "domain", target, "")

        await update.message.reply_text(text, parse_mode="HTML")
    except Exception as e:
        logger.error("Domain lookup failed for %s: %s", target, e)
        await update.message.reply_text("❌ Lookup failed. Please try again later.")


async def bulk_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not rate_limiter.is_allowed(user_id):
        await update.message.reply_text("⏳ Rate limit exceeded. Please wait a moment.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /bulk <ip1> <ip2> ...\nMax 5 addresses.")
        return

    targets = context.args[:5]
    valid_targets = [t for t in targets if _validate_ip(t)]

    if not valid_targets:
        await update.message.reply_text("❌ No valid public IP addresses provided.")
        return

    await update.message.reply_text(f"🔄 Looking up {len(valid_targets)} addresses...")

    results = []
    for target in valid_targets:
        try:
            result = await lookup_ip(target)
            results.append(format_ip_result(result))
        except Exception:
            results.append(f"❌ <b>{target}</b> — lookup failed")

    text = "\n\n{'─' * 30}\n\n".join(results)
    await update.message.reply_text(text, parse_mode="HTML")


async def history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    db_path = context.bot_data.get("db_path", "data/history.db")

    async with Database(db_path) as db:
        records = await db.get_history(user_id, limit=10)

    if not records:
        await update.message.reply_text("📭 No lookup history yet.")
        return

    lines = ["📋 <b>Last 10 lookups:</b>\n"]
    for rec in records:
        lines.append(f"• <code>{rec['target']}</code> ({rec['lookup_type']}) — {rec['created_at']}")

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")
