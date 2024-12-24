from fastapi import FastAPI
from pydantic import BaseModel
from aiogram import Bot
import os

# Инициализация бота
token = os.getenv("TOKEN")
bot = Bot(token=token)

# Инициализация FastAPI
app = FastAPI()

# Модель данных для запроса
class MessageData(BaseModel):
    user_id: int
    message: str

# Маршрут для отправки сообщений через бота
@app.post("/send_message")
async def send_message(data: MessageData):
    await bot.send_message(chat_id=data.user_id, text=data.message)
    return {"status": "success", "message": "Сообщение отправлено!"}