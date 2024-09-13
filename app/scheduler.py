from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database.requests import send_day_text, send_comment_keyboard

scheduler = AsyncIOScheduler()

#Глобально тут надо еще добавить чтобы чел мог выбирать время отправки сообщений своих и время оставления комментов тоже ну прост по мск въебать
#Короче тут я хуй подзабил, но оно вроде и не надо(ну короче если вот юзер зайдет в 5.00, то в 8.00 у него уже будет второй день хз круто это или нет)
def add_send_day_text_job(user_id, bot):
    job_id = f"send_day_text_{user_id}"
    if scheduler.get_job(job_id) is None:
        scheduler.add_job(send_day_text, trigger=CronTrigger(hour=8, minute=0), args=[user_id, bot], id=job_id)


def schedule_comment_keyboard_job(user_id, bot):
    job_id = f"comment_keyboard_{user_id}"
    if scheduler.get_job(job_id) is None:
        scheduler.add_job(send_comment_keyboard, trigger=CronTrigger(hour=8, minute=0), args=[user_id, bot], id=job_id)


def start_scheduler():
    scheduler.start()
