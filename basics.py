from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3
import datetime as dt

# Функция для команда старта запоминания


def start(update, context):
    update.message.reply_text('Начинаю запоминать ваши дела')
    return 1


# Функция для команды, выводящей информацию об основных командах

def help(update, context):
    update.message.reply_text('/start - команда, дающая старт диалогу,'
                              ' в котором бот начинает запоминать дела принимая'
                              ' сообщения в формате <Дело> <Год-месяц-день> <Часы:минуты>'
                              ''
                              '/stop – команда, заканчивающая запоминание дел'
                              ''
                              '/plans – команда, принимающая на вход один'
                              ' из аргументов(day, week, month, year, all)'
                              ' и выводящая все дела в данном временном промежутке'
                              '/del - команда позволяющая убрать дело из списка напоминаний')


def stop_planning(update, context):
    update.message.reply_text('Заканчиваю запоминать')
    return ConversationHandler.END