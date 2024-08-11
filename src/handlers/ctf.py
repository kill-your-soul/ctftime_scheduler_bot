from aiogram.types import Message
from aiogram.fsm.storage import FSMContext

async def start(message: Message, state: FSMContext):
    await message.answer("Hello! I am a bot that will send you information about upcoming CTF events.")