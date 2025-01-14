from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.database.models import Message, async_session
from aiogram import Bot
import os
from datetime import datetime, timezone
from app.database.requests import save_user_message

app = FastAPI()
token = os.getenv("TOKEN")
bot = Bot(token=token)

class MessageData(BaseModel):
    user_id: int
    message: str

class MessageResponse(BaseModel):
    id: int
    tg_id: int
    message_id: int
    text: str
    timestamp: str
    sender_type: str

    class Config:
        orm_mode = True

async def get_db():
    async with async_session() as session:
        yield session

# Получить список id
@app.get("/users", response_model=list[int])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message.tg_id).distinct())
    return [row[0] for row in result.all()]

# Получить сообщения юзера
@app.get("/messages/{user_id}", response_model=list[MessageResponse])
async def get_user_messages(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message).where(Message.tg_id == user_id))
    messages = result.scalars().all()
    for message in messages:
        message.timestamp = message.timestamp.isoformat()
    return messages

# Сохранение в бд
@app.post("/send_message")
async def send_message(data: MessageData):
    timestamp = datetime.now(timezone.utc)

    sent_message = await bot.send_message(chat_id=data.user_id, text=data.message)

    await save_user_message(
        tg_id=data.user_id,
        message_id=sent_message.message_id,
        text=data.message,
        timestamp=timestamp,
        sender_type="bot"
    )

    return {"status": "success", "message": "Message sent and saved!"}