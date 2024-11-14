import asyncio

from db.src.db import DB
from bot.src.bot import TG_Bot
from db.src.storage import UserStorage
from utils.src.config_reader import config


async def main():
    db = DB(
        host=config.host.get_secret_value(),
        port=config.port.get_secret_value(),
        login=config.login.get_secret_value(),
        password=config.password.get_secret_value(),
        database=config.database.get_secret_value(),
    )
    await db.init()

    user_storage = UserStorage(db)
    await user_storage.init()

    bot = TG_Bot(
        bot_token=config.tgbot_api_key.get_secret_value(),
        user_storage=user_storage,
    )
    await bot.init()

    try:
        await bot.start()
    except Exception as e:
        print(f"Bot error: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
