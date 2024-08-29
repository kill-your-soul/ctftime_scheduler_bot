from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from events import get_events, send_ctf_time_event, send_ctf_time_event_split
from keyboards.menu import back_button, main_menu


async def start_handler(message: Message, _state: FSMContext) -> None:
    keyboard = main_menu()
    await message.answer("Hello! I am a bot that will send you information about upcoming CTF events.", reply_markup=keyboard)


# async def upcoming_ctfs(message: Message, state: FSMContext):
#     keyboard = back_button()
#     ctftime = get_events()
#     for event in ctftime.events:
#         start_time = event.start.astimezone(timezone("Europe/Moscow")).strftime(
#             "%A, %d %B %Y %H:%M"
#         )
#         end_time = event.finish.astimezone(timezone("Europe/Moscow")).strftime(
#             "%A, %d %B %Y %H:%M"
#         )
#         if event.logo == '':
#             await message.answer(
#                 f"{event.title} — {start_time} — {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nFormat: {event.format}\nWeight: {event.weight}\nDuration: {event.duration.days} days {event.duration.hours} hours",
#             )
#         else:
#             await message.answer_photo(
#             photo=str(event.logo),
#             caption=f"{event.title} — {start_time} — {end_time}\nurl: {event.url}\nctftime url: {event.ctftime_url}\nFormat: {event.format}\nWeight: {event.weight}\nDuration: {event.duration.days} days {event.duration.hours} hours",
#         )
#     await message.answer("That's all. Choose wisely", reply_markup=keyboard)


async def upcoming_today_ctf(message: Message, _state: FSMContext) -> None:
    ctftime = await get_events(start=datetime.now(), end=datetime.now() + timedelta(1))
    keyboard = back_button()
    if len(ctftime.events) == 0:
        await message.answer("No events today")
    for event in ctftime.events:
        await send_ctf_time_event(message.bot, event, message.chat.id)
    await message.answer("That's all. Choose wisely", reply_markup=keyboard)

async def upcoming_week_ctfs(message: Message, _state: FSMContext) -> None:
    ctftime = await get_events(start=datetime.now(), end=datetime.now() + timedelta(7))
    keyboard = back_button()
    if len(ctftime.events) == 0:
        await message.answer("No events this week")
    for event in ctftime.events:
        await send_ctf_time_event(message.bot, event, message.chat.id)
    await message.answer("That's all. Choose wisely", reply_markup=keyboard)

async def upcoming_month_ctfs(message: Message, _state: FSMContext) -> None:
    ctftime = await get_events(start=datetime.now(), end=datetime.now() + timedelta(30))
    keyboard = back_button()
    if len(ctftime.events) == 0:
        await message.answer("No events this month")
    await send_ctf_time_event_split(message.bot, ctftime.events, message.chat.id)
    await message.answer("That's all. Choose wisely", reply_markup=keyboard)

async def back(message: Message, _state: FSMContext) -> None:
    keyboard = main_menu()
    await message.answer("Main menu", reply_markup=keyboard)
