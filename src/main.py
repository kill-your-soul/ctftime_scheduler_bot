import logging
from pathlib import Path
from typing import NoReturn
import requests
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, Redis
from loguru import logger
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from core import settings
from schemas import CTFTimeEvent, CTFTimeResponse
import handlers
from events import get_events, send_ctf_time_event


def setup_handlers(dp: Dispatcher):
    dp.include_router(handlers.setup_handlers())


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.log(level, record.getMessage())


@logger.catch
async def main(bot: Bot) -> NoReturn:
    # logging.getLogger("aiogram").setLevel(logging.DEBUG)
    # logging.getLogger("aiogram").addHandler(InterceptHandler())
    # logging.getLogger("asyncio").setLevel(logging.DEBUG)
    # logging.getLogger("asyncio").addHandler(InterceptHandler())
    base_dir = Path(__file__).resolve().parent.parent
    logger.add(base_dir / "logs.log", level="DEBUG")
    redis = Redis(host=settings.REDIS_HOST)
    storage = RedisStorage(redis)
    dp = Dispatcher(storage=storage)
    setup_handlers(dp)
    await schedule(bot)
    logger.info("Starting bot")
    
    # schenduler.add_job(schedule, "interval", days=7)
    await dp.start_polling(bot)
    # while True:
    #     await asyncio.sleep(1)


async def schedule(bot: Bot):
    ctftime: CTFTimeResponse = await get_events(start=datetime.now(), end=datetime.now() + timedelta(7))
    for event in ctftime.events:
        try:
            await send_ctf_time_event(bot, event, settings.CHAT_ID, settings.MESSAGE_THREAD_ID)
        except Exception as e:
            print(e)
            continue



if __name__ == "__main__":
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    schenduler = AsyncIOScheduler()
    schenduler.add_job(schedule, "interval", days=7, args=(bot,))
    schenduler.start()
    try:
        asyncio.run(main(bot))
    except KeyboardInterrupt:
        sys.exit(0)
