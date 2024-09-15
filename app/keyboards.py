from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def are_you_ready_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="да", callback_data="first_yes_button"))
    keyboard.add(InlineKeyboardButton(text="нет", callback_data="first_no_button"))
    return keyboard.adjust(2).as_markup()


async def keyboard_for_comments():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Здесь можно оставить комментарий", callback_data="comment_button"))
    return keyboard.adjust(2).as_markup()


async def keyboard_for_communication():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Связь с куратором", callback_data="communicate_button"))
    return keyboard.adjust(2).as_markup()