from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.requests import send_day_text

scheduler = AsyncIOScheduler()

def add_send_day_text_job(user_id, bot, interval_seconds=5):
    scheduler.add_job(send_day_text, trigger='interval', seconds=interval_seconds, args=[user_id, bot])

def start_scheduler():
    scheduler.start()
