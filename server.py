from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.database.models import Message, async_session  # Импортируем модель Message и сессию async_session
from aiogram import Bot
import os

# Инициализация FastAPI
app = FastAPI()
token = os.getenv("TOKEN")
bot = Bot(token=token)

# Модель данных для запроса
class MessageData(BaseModel):
    user_id: int
    message: str

# Модель данных для ответа (Message) на запрос
class MessageResponse(BaseModel):
    id: int
    tg_id: int
    message_id: int
    text: str
    timestamp: str  # Ожидаем, что timestamp уже будет строкой

    class Config:
        orm_mode = True  # Это нужно для сериализации SQLAlchemy объектов в JSON

# Функция для получения сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session

# Маршрут для получения всех сообщений из базы данных
@app.get("/messages", response_model=list[MessageResponse])
async def get_messages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message))
    messages = result.scalars().all()
    for message in messages:
        message.timestamp = message.timestamp.isoformat()  # Преобразуем datetime в строку
    return messages

# Маршрут для отправки сообщений через бота
@app.post("/send_message")
async def send_message(data: MessageData):
    await bot.send_message(chat_id=data.user_id, text=data.message)
    return {"status": "success", "message": "Сообщение отправлено!"}

