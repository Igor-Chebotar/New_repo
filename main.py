from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3
import datetime as dt
from planning import *
from plans import *
from delite import *
from basics import *
from .secret import TOKEN


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, planning)],
        },
        fallbacks=[CommandHandler('stop', stop_planning)]
    )
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('stop', stop_planning))
    dp.add_handler(CommandHandler("plans", plans_for_something, pass_args=True))
    dp.add_handler(CommandHandler("del", del_reminder, pass_args=True))
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
