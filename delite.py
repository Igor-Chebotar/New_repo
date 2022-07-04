from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3
import datetime as dt

# Функция для команды удаления напоминания и дела из списка


def del_reminder(update, context):
    plan = context.args
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM Plans WHERE plan=?""", (' '.join(plan),))
    con.commit()
    job_removed = remove_job_if_exists(
            str(plan),
            context
        )
    if job_removed:
        update.message.reply_text('Дело убрано из списка напоминаний')
    else:
        update.message.reply_text('Такого дела не было в списке')

# Удаляем напоминание по имени


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True