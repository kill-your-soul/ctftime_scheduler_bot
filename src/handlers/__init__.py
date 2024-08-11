from aiogram import Router
from aiogram.filters import CommandStart
from . import ctf

def setup_handlers() -> Router:
    router = Router()
    
    router.message.register(ctf.start, CommandStart())

    return router