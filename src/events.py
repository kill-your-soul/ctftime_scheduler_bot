from datetime import datetime

from aiogram import Bot
from aiogram.utils.media_group import MediaGroupBuilder
from aiohttp import ClientSession
from loguru import logger
from pytz import timezone

from schemas import CTFTimeEvent, CTFTimeResponse


async def get_events(start: datetime, end: datetime) -> CTFTimeResponse:
    """Get upcoming CTF events from ctftime.org.

    Returns
    -------
        CTFTimeResponse: A pydantic model containing the events

    """
    logger.info("Getting events")
    # start = datetime.now() + timedelta(7)
    # end = start + timedelta(7)
    end = int(end.timestamp())
    start = int(start.timestamp())
    url = f"http://ctftime.org/api/v1/events/?limit=100&start={start}&finish={end}"
    # session = requests.Session()
    # req = requests.Request("GET", url=url, headers=headers).prepare()
    # response = session.send(request=req)
    # client = ClientSession()
    # response = client.get(url)
    async with ClientSession() as session, session.get(url, headers={"Host": "ctftime.org"}) as response:
        logger.debug(f"Got response: {response.status}")
        ctftime: CTFTimeResponse = CTFTimeResponse(events=await response.json())

    return ctftime


async def send_ctf_time_event(bot: Bot, event: CTFTimeEvent, chat_id: int | str, thread_id: int | None = None) -> None:
    start_time = event.start.astimezone(timezone("Europe/Moscow")).strftime(
        "%A, %d %B %Y %H:%M",
    )
    end_time = event.finish.astimezone(timezone("Europe/Moscow")).strftime(
        "%A, %d %B %Y %H:%M",
    )
    if event.logo == "":
        await bot.send_message(
            chat_id,
            f"{event.title} {start_time} {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nFormat: {event.format}\nWeight: {event.weight}\nDuration: {event.duration.days} days {event.duration.hours} hours",  # noqa: E501
            message_thread_id=thread_id,
        )
        return
    message = f"{event.title} {start_time} {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nFormat: {event.format}\nWeight: {event.weight}\nDuration: {event.duration.days} days {event.duration.hours} hours"  # noqa: E501
    await bot.send_photo(
        chat_id,
        photo=event.logo,
        caption=message,
        message_thread_id=thread_id,
    )


async def send_ctf_time_event_split(
    bot: Bot, events: list[CTFTimeEvent], chat_id: int | str, thread_id: int | None = None
) -> None:
    for i in range(0, len(events), 5):
        media_group = MediaGroupBuilder()
        caption = ""
        for event in events[i : i + 5]:
            if event.logo == "":
                start_time = event.start.astimezone(timezone("Europe/Moscow")).strftime(
                    "%A, %d %B %Y %H:%M",
                )
                end_time = event.finish.astimezone(timezone("Europe/Moscow")).strftime(
                    "%A, %d %B %Y %H:%M",
                )
                caption += f"{event.title} {start_time} {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nDuration: {event.duration.days} days {event.duration.hours} hours\n\n"  # noqa: E501
                media_group.add_photo(
                    "https://yt3.googleusercontent.com/ytc/AIdro_mF7DqLwvW5TfkZMbR1DxJQJyJ-cdP2fyTDOF_yMvZJMYE=s900-c-k-c0x00ffffff-no-rj"
                )
                continue
            start_time = event.start.astimezone(timezone("Europe/Moscow")).strftime(
                "%A, %d %B %Y %H:%M",
            )
            end_time = event.finish.astimezone(timezone("Europe/Moscow")).strftime(
                "%A, %d %B %Y %H:%M",
            )
            caption += f"{event.title} {start_time} {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nDuration: {event.duration.days} days {event.duration.hours} hours\n\n"
            media_group.add_photo(event.logo)
        logger.debug(f"caption: {caption}")
        logger.debug(f"Len of caption: {caption.__len__()}")
        media_group.caption = caption
        logger.debug(media_group.build())
        await bot.send_media_group(chat_id, media=media_group.build(), message_thread_id=thread_id)
