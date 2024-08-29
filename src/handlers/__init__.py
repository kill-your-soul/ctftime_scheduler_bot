from aiogram import F, Router
from aiogram.filters import CommandStart

from . import ctf


def setup_handlers() -> Router:
    router = Router()
    router.message.register(ctf.start_handler, CommandStart())
    router.message.register(ctf.upcoming_today_ctf, F.text == "☀️ Today")
    router.message.register(ctf.upcoming_week_ctfs, F.text == "📆 Next week")
    router.message.register(ctf.upcoming_month_ctfs, F.text == "🈷️ Next month")
    router.message.register(ctf.back, F.text == "🔙 Back")
    return router
