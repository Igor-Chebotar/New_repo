from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3
import datetime as dt

# Функция, которая записывает дела в базу данных


def planning(update, context):
    user_id = update.message.from_user['id']

    text = update.message.text.split(' ')
    date = dt.date(int(text[-2].split('-')[0]), int(text[-2].split('-')[1]), int(text[-2].split('-')[2]))
    time = dt.time(int(text[-1].split(':')[0]), int(text[-1].split(':')[1], 00))
    if dt.datetime.now() > dt.datetime.combine(date, time):
        update.message.reply_text('Запланировать на прошлое, к сожалению, нельзя')
        return
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO Plans (user_id, date, time, plan) VALUES (?, ?, ?, ?)""",
                (str(user_id), str(date), str(time), ' '.join(text[:-2])))
    con.commit()
    set_reminder(update, context, [' '.join(text[:-2]), date, time])
    update.message.reply_text('Записал')

# Функция постановки напоминания


def set_reminder(update, context, plan):
    chat_id = update.message.chat_id
    year, month, day = str(plan[1]).split('-')
    hour, minute, seconds = str(plan[2]).split(':')
    time = dt.datetime(int(year), int(month), int(day), int(hour), int(minute), 0)
    context.job_queue.run_once(
        reminder,
        time,
        context=(chat_id, str(plan[0])),
        name=str(plan[0])
    )


def reminder(context):
    job = context.job
    context.bot.send_message(job.context[0], text=f'Напоминаю о деле - {job.context[1]}')