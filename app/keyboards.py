from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Связь с куратором")],
        [KeyboardButton(text="Вывести историю состояний")]
    ],
    resize_keyboard=True,
    input_field_placeholder="юпийо"
)

async def are_you_ready_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="да", callback_data="first_yes_button"))
    keyboard.add(InlineKeyboardButton(text="нет", callback_data="first_no_button"))
    return keyboard.adjust(2).as_markup()


async def keyboard_for_comments():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Здесь можно оставить комментарий", callback_data="comment_button"))
    return keyboard.adjust(5).as_markup()


async def keyboard_for_communication():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Связь с куратором", callback_data="communicate_button"))
    return keyboard.adjust(2).as_markup()


async def keyboard_for_rate_user_state():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🟥", callback_data="state_1"))
    keyboard.add(InlineKeyboardButton(text="🟧", callback_data="state_2"))
    keyboard.add(InlineKeyboardButton(text="🟨", callback_data="state_3"))
    keyboard.add(InlineKeyboardButton(text="🟩", callback_data="state_4"))
    keyboard.add(InlineKeyboardButton(text="🟦", callback_data="state_5"))
    return keyboard.adjust(5).as_markup()


