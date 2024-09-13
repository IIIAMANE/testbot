from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from app.scheduler import add_send_day_text_job,schedule_comment_keyboard_job
from app.state import Comment_for_day


import app.keyboards as kb
import app.database.requests as rq
import app.state as st

from text import days_dictionary

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message):
    await rq.set_user(message.from_user.id)
    bot = message.bot
    day = await rq.get_day(message.from_user.id)

    if day == 0:
        photo_url = "https://i.pinimg.com/736x/09/20/6b/09206b54664edda9193e1fdad221b7c4--hermione-cat-comics.jpg"
        caption = "Всем привет)\nТут чето типо описания будет"
        await rq.send_photo_to_user(bot, message.chat.id, photo_url, caption)
        await message.answer("Хотите ли вы пройти нашего бота\nну чет такое хз о.О", reply_markup=await kb.are_you_ready_button())
    else:
        add_send_day_text_job(message.from_user.id, bot)
        schedule_comment_keyboard_job(message.from_user.id, bot)
        await message.answer("Привет! Продолжаем с того места, где ты остановился.")


@router.callback_query(F.data == "first_no_button")
async def user_not_ready(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Пипяу..")


@router.callback_query(F.data == "first_yes_button")
async def main_day_handler(callback: CallbackQuery):
    await callback.answer("")
    await rq.send_day_text(callback.from_user.id, callback.bot)
    add_send_day_text_job(callback.from_user.id, callback.bot)
    schedule_comment_keyboard_job(callback.from_user.id, callback.bot)


@router.callback_query(F.data == "comment_button")
async def comment_text(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Comment_for_day.user_comment)
    await callback.answer("")
    await callback.message.answer("Напиши свой комментарий к сегодняшнему дню")


@router.message(Comment_for_day.user_comment)
async def save_user_comment(message: Message, state: FSMContext):
    await state.update_data(comment_text = message.text)
    data = await state.get_data()
    print(data.get('comment_text'))


    



