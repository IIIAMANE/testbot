from app.database.models import async_session
from sqlalchemy import select, update
from app.database.models import User
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


async def get_day(tg_id: int):
    async with async_session() as session:
        day = await session.scalar(select(User.day).where(User.tg_id == tg_id))
        return day


async def increment_day(tg_id: int):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(day=User.day + 1)
        )
        await session.commit()


async def send_day_text(user_id, bot):
    day = await get_day(user_id)
    message = days_dictionary.get(day, "Нет информации по этому дню")
    await bot.send_message(chat_id=user_id, text=message)
    await increment_day(user_id)


async def send_comment_keyboard(user_id: int, bot):
    await bot.send_message(chat_id=user_id,text="оставь коммент", reply_markup=await kb.keyboard_for_comments())
