import requests
from datetime import datetime, timedelta
from time import time
from pprint import pprint
from aiogram import Bot
from aiogram.enums import ParseMode
import os
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
MESSAGE_THREAD_ID = os.environ.get('MESSAGE_THREAD_ID')



async def main():
    schenduler = AsyncIOScheduler()
    schenduler.add_job(bot, 'interval', days=7)
    schenduler.start()

async def bot():
    headers = {"Host": "ctftime.org"}
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # print(bot)
    start = datetime.now()
    end = start + timedelta(7)
    end = int(end.timestamp())
    start = int(start.timestamp())
    url = f'http://ctftime.org/api/v1/events/?limit=100&start={start}&finish={end}'
    # print(url)
    session = requests.Session()
    req = requests.Request("GET", url=url, headers=headers).prepare()
    res = session.send(request=req)

    # pprint(res.json()[0])
    for json in res.json():
        try:
            await send_message(bot, json)
        except Exception as e:
            print(e)
            continue
    session.close()
    # await send_message(bot, res.json()[0])

async def send_message(bot: Bot, json):
    message = f'{json["title"]} {json["start"]} {json["finish"]}\n\t\t\t\t\t\tUrl: {json["url"]}\n\t\t\t\t\t\tFormat: {json["format"]}\n\t\t\t\t\t\tDuration: {json["duration"]["days"]} days {json["duration"]["hours"]} hours\n<a href=\"{json["logo"]}\"></a>'
    print(message)
    # await bot.send_message(CHAT_ID, message, message_thread_id=3, parse_mode=ParseMode.HTML)
    await bot.send_photo(CHAT_ID, photo=json["logo"], caption=message, message_thread_id=3)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
