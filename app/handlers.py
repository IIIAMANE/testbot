from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq
import app.state as st

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
    elif day != 0:
        await message.answer(
            "Ну тут я пока хз че написать, чето на уровне йоу привет еще раз мб задание повторить"
        )


#Если чел нажал нет
@router.callback_query(F.data == "user_not_ready")
async def user_not_ready(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Пипяу..")


# Ну дальше писать через да и открывать состояние в теории