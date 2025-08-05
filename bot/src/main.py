import asyncio
import logging
import os

from bot import BotApp
from db import db_manager


def setup_logging() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    os.makedirs("/app/logs", exist_ok=True)
    f_handler = logging.FileHandler("/app/logs/bot.log")
    f_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


async def main():
    logger = setup_logging()
    bot = BotApp(db_manager, logger)

    try:
        await bot.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")


if __name__ == "__main__":
    asyncio.run(main())
