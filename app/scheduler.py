from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.requests import send_day_text

scheduler = AsyncIOScheduler()

def add_send_day_text_job(user_id, bot, interval_seconds=5000000):
    job_id = f"send_day_text_{user_id}"
    if scheduler.get_job(job_id) is None:
        scheduler.add_job(send_day_text, trigger='interval', seconds=interval_seconds, args=[user_id, bot], id=job_id)



def start_scheduler():
    scheduler.start()
