import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import random as r
import sqlite3
def wordbib():
    b=r.randint(1,74)
    conn = sqlite3.connect('bible.db')
    curs = conn.cursor()
    sql1 = "select max(actual_chapter_no) from verses where book_no='%d'"%(b)
    curs.execute(sql1)
    maxcount= curs.fetchall()
    f = maxcount
    out = [item for t in f for item in t] 
    c=r.randint(1,out[0])
    sql2 = "select max(verse_no) from verses where book_no='%d' and actual_chapter_no='%d'"%(b,c)
    curs.execute(sql2)
    maxv=curs.fetchall()
    g = maxv
    out = [item for t in g for item in t]
    v=r.randint(1,out[0])
    sql = "select verse,book from verses where book_no='%d' and actual_chapter_no='%d' and verse_no='%d' "%(b,c,v)
    curs.execute(sql)
    results = curs.fetchall()
    for row in results:
        str2 = str("\"")+row[0]+str("\"\n")+ row[1]+str(" ")+str(c)+str(":")+str(v)+str("\n\nഅദ്യായം മുഴുവൻ വായിക്കാൻ ശ്രമിക്കുക")
    return(str2)


def start(update, context):
    str1=wordbib()
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bible bot!")
    keyboard = [[InlineKeyboardButton("Today's Word", callback_data='1'),
                 InlineKeyboardButton("Today's Saint", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Praise the Lord', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == str(1):
        query.edit_message_text(text=wordbib())

    if query.data ==str(2):
        query.edit_message_text(text='Published later')
    



def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("943688480:AAGj4iS5oWGb8CGX9eaU4YzlBbvwrf1U0t8", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
