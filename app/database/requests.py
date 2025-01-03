from datetime import datetime

from app.database.models import async_session
from sqlalchemy import select, update

from app.database.models import User, Message, User_state
from text import days_dictionary

import app.keyboards as kb



async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def send_photo_to_user(bot, chat_id, photo_url, caption):
    await bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)


async def get_day(tg_id: int):
    async with async_session() as session:
        day = await session.scalar(select(User.day).where(User.tg_id == tg_id))
        return day
    

async def get_user_state_history(tg_id: int):
    async with async_session() as session:
        user_state_history = await session.scalar(select(User_state.state).where(User_state.tg_id == tg_id))
        return user_state_history


async def increment_day(tg_id: int):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(day=User.day + 1)
        )
        await session.commit()


async def send_day_text(user_id, bot):
    day = await get_day(user_id)
    message = days_dictionary.get(day, "Нет информации по этому дню")
    await bot.send_message(chat_id=user_id,text=message, reply_markup=await kb.keyboard_for_communication())
    await increment_day(user_id)


async def send_comment_keyboard(user_id: int, bot):
    await bot.send_message(chat_id=user_id,text="оставь коммент(если хочешь)", reply_markup=await kb.keyboard_for_comments())


async def send_state_keyboard(user_id: int, bot):
    await bot.send_message(chat_id=user_id,text="оцени состояние квадратиками(если хочешь)", reply_markup=await kb.keyboard_for_rate_user_state())


async def save_user_comment(tg_id: int, comment: str) -> None:
    async with async_session() as session:
        day = await session.scalar(select(User.day).where(User.tg_id == tg_id))
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if user.comments:
            updated_comments = f"{user.comments}\n\n{day}: {comment}"
        else:
            updated_comments = f"{day}: {comment}"

        await session.execute(update(User).where(User.tg_id == tg_id).values(comments=updated_comments))
        await session.commit()


async def save_user_state(tg_id: int, rate: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        day = user.day
        user_state = await session.scalar(select(User_state).where(User_state.tg_id == tg_id))

        if user_state:
            updated_state = f"{user_state.state}, {day}:{rate}"
            await session.execute(update(User_state).where(User_state.tg_id == tg_id).values(state=updated_state))
        else:
            updated_state = f"{day}:{rate}"
            new_state = User_state(tg_id=tg_id, state=updated_state)
            session.add(new_state)
        
        await session.commit()


async def save_user_message(tg_id: int, message_id: int, text: str, timestamp: datetime, sender_type: str = "user") -> None:
    async with async_session() as session:
        new_message = Message(tg_id=tg_id, message_id=message_id, text=text, timestamp=timestamp, sender_type=sender_type)
        session.add(new_message)
        await session.commit()