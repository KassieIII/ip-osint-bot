import os
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.handlers import (
    start_handler,
    help_handler,
    ip_handler,
    domain_handler,
    bulk_handler,
    history_handler,
)
from bot.database import Database

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    db_path = os.getenv("DB_PATH", "data/history.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app = ApplicationBuilder().token(token).build()

    # Store DB path in bot_data for handlers to access
    app.bot_data["db_path"] = db_path

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("ip", ip_handler))
    app.add_handler(CommandHandler("domain", domain_handler))
    app.add_handler(CommandHandler("bulk", bulk_handler))
    app.add_handler(CommandHandler("history", history_handler))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
