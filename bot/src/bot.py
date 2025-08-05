import logging

from redis.asyncio import Redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties

from utils import settings
from db import DatabaseManager
from routers import main_router
from middlewares import (
    BotMiddleware,
    RedisMiddleware,
    LoggingMiddleware,
    RepositoriesMiddleware,
)


class BotApp:
    def __init__(self, db_manager: DatabaseManager, logger: logging.Logger):
        self.logger = logger
        self.db_manager = db_manager
        self.bot = None
        self.dp = None

    async def _setup_bot(self) -> None:
        self.bot = Bot(
            token=settings.telegram_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        print(await self.bot.get_me())
        redis = Redis(
            host=settings.redis_host.get_secret_value(), port=settings.redis_port
        )
        storage = RedisStorage(redis=redis)
        self.dp = Dispatcher(storage=storage)

        for event_type in [self.dp.message, self.dp.callback_query]:
            event_type.middleware(BotMiddleware(self.bot))
            event_type.outer_middleware(LoggingMiddleware(self.logger))
            event_type.outer_middleware(RedisMiddleware(self.db_manager))
            event_type.outer_middleware(RepositoriesMiddleware(self.db_manager))

        self.dp.include_router(main_router)

    async def _set_commands(self):
        if self.bot:
            await self.bot.set_my_commands(
                commands=[
                    BotCommand(command="start", description="Начать работу с ботом"),
                ]
            )

    async def start(self):
        try:
            await self.db_manager.init()
            await self._setup_bot()
            await self._set_commands()

            if self.bot and self.dp:
                self.logger.info("Starting polling...")
                await self.dp.start_polling(self.bot)
            else:
                self.logger.error("Bot or dispatcher is None, cannot start polling")
        except Exception as e:
            self.logger.error(f"Error while starting bot: {e}", exc_info=True)
        finally:
            await self.db_manager.close()
