from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def are_you_ready_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="да", callback_data="go_to_day_1"))
    keyboard.add(InlineKeyboardButton(text="нет", callback_data="user_not_ready"))
    return keyboard.adjust(2).as_markup()