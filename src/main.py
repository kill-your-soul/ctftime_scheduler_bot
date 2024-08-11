import requests
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from src.core import settings
from schemas import CTFTimeEvent, CTFTimeResponse


async def main():
    await schedule()
    logger.info("Starting bot")
    schenduler = AsyncIOScheduler()
    schenduler.add_job(schedule, "interval", days=7)
    schenduler.start()
    while True:
        await asyncio.sleep(1)


async def schedule():
    headers = {"Host": "ctftime.org"}
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    start = datetime.now()
    end = start + timedelta(7)
    end = int(end.timestamp())
    start = int(start.timestamp())
    url = f"http://ctftime.org/api/v1/events/?limit=100&start={start}&finish={end}"
    session = requests.Session()
    req = requests.Request("GET", url=url, headers=headers).prepare()
    response = session.send(request=req)
    ctftime: CTFTimeResponse = CTFTimeResponse(events=response.json())
    for event in ctftime.events:
        try:
            await send_message(bot, event)
        except Exception as e:
            print(e)
            continue
    session.close()


async def send_message(bot: Bot, event: CTFTimeEvent):
    start_time = event.start.astimezone(timezone("Europe/Moscow")).strftime("%A, %d %B %Y %H:%M")
    end_time = event.finish.astimezone(timezone("Europe/Moscow")).strftime("%A, %d %B %Y %H:%M")

    print(start_time)
    print(end_time)


# async def send_message(bot: Bot, json):
#     start_time = datetime.fromisoformat(json["start"].replace("Z", "+00:00")).astimezone(timezone('Europe/Moscow')).strftime("%A, %d %B %Y %H:%M")
#     end_time = datetime.fromisoformat(json["finish"].replace("Z", "+00:00")).astimezone(timezone('Europe/Moscow')).strftime("%A, %d %B %Y %H:%M")
#     message = f'{json["title"]} {start_time} {end_time}\n\t\t\t\t\t\tUrl: {json["url"]}\n\t\t\t\t\t\tctftime url: {json["ctftime_url"]}\n\t\t\t\t\t\tFormat: {json["format"]}\n\t\t\t\t\t\tWeight: {json["weight"]}\n\t\t\t\t\t\tDuration: {json["duration"]["days"]} days {json["duration"]["hours"]} hours\n<a href="{json["logo"]}"></a>'
#     print(message)
#     await bot.send_photo(
#         settings.CHAT_ID, photo=json["logo"], caption=message, message_thread_id=settings.MESSAGE_THREAD_ID
#     )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
