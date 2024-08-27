from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    # builder.button(text="📅 Upcoming CTFs")
    builder.button(text="☀️ Today")
    builder.button(text="📆 Next week")
    builder.button(text="🈷️ Next month")
    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

def back_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔙 Back")
    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)