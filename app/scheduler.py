from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database.requests import send_day_text, send_comment_keyboard

scheduler = AsyncIOScheduler()

def add_send_day_text_job(user_id, bot, interval_seconds=5000000):
    job_id = f"send_day_text_{user_id}"
    if scheduler.get_job(job_id) is None:
        scheduler.add_job(send_day_text, trigger='interval', seconds=interval_seconds, args=[user_id, bot], id=job_id)


def schedule_comment_keyboard_job(user_id, bot):
    job_id = f"comment_keyboard_{user_id}"
    if scheduler.get_job(job_id) is None:
        scheduler.add_job(send_comment_keyboard, trigger=IntervalTrigger(days=1, start_date='2024-09-13 15:03:15'), args=[user_id, bot], id=job_id)


def start_scheduler():
    scheduler.start()
