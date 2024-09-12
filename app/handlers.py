from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler import add_send_day_text_job


import app.keyboards as kb
import app.database.requests as rq
import app.state as st

from text import days_dictionary

router = Router()


@router.message(CommandStart)
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
        await message.answer("Ну тут я пока хз че написать, чето на уровне йоу привет еще раз мб задание повторить")


@router.callback_query(F.data == "first_no_button")
async def user_not_ready(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Пипяу..")


#Если чел перезапустит бота, то он еще раз не нажмет да, т.е надо делать запуск этого прикола(add_send_day_text_job) не в функции, а где то глобально
# и добавлять проверку на уровне если день != 0, тогда и после рестарта бота все будет воркать в теории
# Ну короче придумаешь как реализовать, главное с импортами разобрался + еще надо второе сообщение отправлять типочкам и к нему клеить клаву
# оставь отзыв чет такое или как день прошел напиши там пиу пиу
@router.callback_query(F.data == "first_yes_button")
async def main_day_handler(callback: CallbackQuery):
    await callback.answer("")
    await rq.send_day_text(callback.from_user.id, callback.bot)
    add_send_day_text_job(callback.from_user.id, callback.bot)


    



