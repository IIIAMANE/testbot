import pytz

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.scheduler import add_send_day_text_job,schedule_comment_keyboard_job, add_send_state_keyboard


import app.keyboards as kb
import app.database.requests as rq
import app.state as st

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message):
    await rq.set_user(message.from_user.id)
    bot = message.bot
    day = await rq.get_day(message.from_user.id)
    await message.answer("негры", reply_markup=await kb.keyboard_for_rate_user_state())
    await message.answer("юпийо(тестовое сообщение, чтобы мейн клаву прицепить)", reply_markup=kb.main)
    if day == 0:
        photo_url = "https://i.pinimg.com/736x/09/20/6b/09206b54664edda9193e1fdad221b7c4--hermione-cat-comics.jpg"
        caption = "Всем привет)\nТут чето типо описания будет"
        await rq.send_photo_to_user(bot, message.chat.id, photo_url, caption)
        await message.answer("Хотите ли вы пройти нашего бота\nну чет такое хз о.О", reply_markup=await kb.are_you_ready_button())
    else:
        add_send_day_text_job(message.from_user.id, bot)
        schedule_comment_keyboard_job(message.from_user.id, bot)
        add_send_state_keyboard(message.from_user.id, bot)
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
    add_send_state_keyboard(callback.from_user.id, callback.bot)


@router.callback_query(F.data == "comment_button")
async def comment_text(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.Comment_for_day.user_comment)
    await callback.answer("")
    await callback.message.answer("Напиши свой комментарий к сегодняшнему дню")


@router.callback_query(F.data.startswith("state_"))
async def handle_rate(callback: CallbackQuery):
    user_state = callback.data.split("_")[1]
    await callback.answer("")
    await callback.message.answer(f'негры {user_state}')
    await rq.save_user_state(callback.from_user.id, user_state)


@router.message(st.Comment_for_day.user_comment)
async def save_user_comment(message: Message, state: FSMContext):
    await state.update_data(comment_text = message.text)
    data = await state.get_data()
    await rq.save_user_comment(message.from_user.id, data.get('comment_text'))
    await state.clear()
    await message.answer("Ваш комментарий доставлен")


@router.callback_query(F.data == "communicate_button")
async def state_for_write_curator(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.Write_to_curator.user_message)
    await callback.answer("")
    await callback.message.answer("Когда напишешь свое сообщение напиши /end, чтобы отправить их куратору(для отмены введи /cancel)")


@router.message(Command("cancel"))
async def cancel_state(message: Message, state: FSMContext):
    await message.answer("Отправка сообщения отменена")
    await state.clear()


@router.message(st.Write_to_curator.user_message)
async def collect_user_message(message: Message, state: FSMContext):
    text = message.text
    if text != '/end':
        data = await state.get_data()
        messages = data.get("messages", [])
        
        timestamp_utc = message.date.replace(tzinfo=pytz.UTC)
        timestamp_msk = timestamp_utc.astimezone(pytz.timezone('Europe/Moscow'))
        
        messages.append({
            'message_id': message.message_id,
            'text': message.text,
            'timestamp': timestamp_msk
        })
        await state.update_data(messages=messages)
        await message.answer("Сообщение сохранено.\nНапиши еще, или отправь /end для завершения(если передумал отправь /cancel)")


    elif text == '/end':
        data = await state.get_data()
        messages = data.get('messages', [])

        if not messages:
            await message.answer("Нет сообщений для отправки.")
            await state.clear()
            return
        
        for msg in messages:
            await rq.save_user_message(
                tg_id=message.from_user.id, message_id=msg['message_id'], text=msg['text'], timestamp=msg['timestamp'])

        await message.answer("Все сообщения отправлены куратору.")
        await state.clear()

    elif text == '/cancel':
        await message.answer("Отправка сообщения отменена")
        await state.clear()


@router.message(F.text == "Связь с куратором")
async def communication_to_curator(message: Message, state: FSMContext):
    await state.set_state(st.Write_to_curator.user_message)
    await message.answer("Когда напишешь свое сообщение напиши /end, чтобы отправить их куратору(для отмены введи /cancel)")


@router.message(F.text == "Вывести историю состояний")
async def print_user_state_history(message: Message, state: FSMContext):
    state_history = await rq.get_user_state_history(message.from_user.id)
    state_emoji = {1: "🟥", 2: "🟧", 3: "🟨", 4: "🟩", 5: "🟦"}
    lines = state_history.split(",")
    result = []
    for line in lines:
        line = line.split(":")
        result.append('-------------------------------')
        result.append(f"день: {line[0]}, состояние: {state_emoji.get(int(line[1]))}")
    formatted_history = "\n".join(result)

    await message.answer(formatted_history)
    
    




