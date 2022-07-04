from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3
import datetime as dt

# Возвращает все дела на день


def plans_for_day(update):
    today = dt.date.today()
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time, plan FROM Plans WHERE date=?""", (str(today),)).fetchall()
    if result:
        for el in result:
            update.message.reply_text(f'{el[0]} {el[1]}')
    else:
        update.message.reply_text('Планов на сегодня пока нет')

# Возвращает все дела на текущую неделю


def plans_for_week(update):
    n = dt.date.today().isoweekday()
    today = dt.date.today()
    delta_time = dt.timedelta(days=1)
    f = False

    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time, plan FROM Plans WHERE date=?""", (str(today),)).fetchall()
    if result:
        update.message.reply_text(str(today))
        f = True
    for el in result:
        update.message.reply_text(f'{el[0]} {el[1]}')
    if 7 - n > 0:
        for i in range(1, 7 - n + 1):
            result = cur.execute("""SELECT time, plan FROM Plans WHERE date=?""",
                                 (str(today + delta_time * i),)).fetchall()
            if result:
                update.message.reply_text(str(today + delta_time * i))
                f = True
            for el in result:
                update.message.reply_text(f'{el[0]} {el[1]}')
    if not f:
        update.message.reply_text('Планов на эту неделю пока нет')

# Возвращает все дела на текущий месяц


def plans_for_month(update):
    today = dt.date.today()
    delta_time = dt.timedelta(days=1)
    f = False

    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT time, plan FROM Plans WHERE date=?""", (str(today),)).fetchall()
    if result:
        update.message.reply_text(str(today))
        f = True
    for el in result:
        update.message.reply_text(f'{el[0]} {el[1]}')
    i = 1
    while str(today).split('-')[1] == str(today + delta_time * i).split('-')[1]:
        result = cur.execute("""SELECT time, plan FROM Plans WHERE date=?""",
                             (str(today + delta_time * i),)).fetchall()
        if result:
            update.message.reply_text(str(today + delta_time * i))
            f = True
        for el in result:
            update.message.reply_text(f'{el[0]} {el[1]}')
        i += 1
    if not f:
        update.message.reply_text('Планов на этот месяц пока нет')

# Возвращает все дела на текущий год


def plans_for_year(update):
    today = dt.date.today()
    user_id = update.message.from_user['id']
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT date, time, plan FROM Plans WHERE user_id=?""", (user_id,)).fetchall()
    if result:
        for el in result:
            if str(el[0]).split('-')[0] == str(today).split('-')[0]:
                update.message.reply_text(el[0])
                update.message.reply_text(f'{el[1]} {el[2]}')
    else:
        update.message.reply_text('Планов на этот год пока нет')

# Возвращает все дела


def all_plans(update):
    user_id = update.message.from_user['id']
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT date, time, plan FROM Plans WHERE user_id=?""", (user_id,)).fetchall()
    if result:
        for el in result:
            update.message.reply_text(el[0])
            update.message.reply_text(f'{el[1]} {el[2]}')
    else:
        update.message.reply_text('Планов пока нет')


def plans_for_something(update, context):
    arg = context.args[0]
    if arg == 'day':
        plans_for_day(update)
    elif arg == 'week':
        plans_for_week(update)
    elif arg == 'month':
        plans_for_month(update)
    elif arg == 'year':
        plans_for_year(update)
    elif arg == 'all':
        all_plans(update)
    else:
        update.message.reply_text('Попробуйте ещё раз, функции /plans '
                                  ' пока можно передать только один из этих аргументов:'
                                  ' day, week, month, year, all')