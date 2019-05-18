#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import logging
import json
import menu
import evaluation
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello, I am CourseRobot, the Telegram interface for Course-O-Meter.com. You do not need "
                              "to add me to chats to view course data. Simply write my name and your query to any chat."
                              "\n\nFor example you can write '@CourseRobot johdatus' (without quotes) to get "
                              "information about any course whose name contains the word 'johdatus'.\n\n"
                              "However, there is more. If you would like to give additional feedback about a course "
                              "and have it published at Course-O-Meter.com, just say /ratecourse!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Available commands:\n\n/ratecourse')


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query.lower()

    if len(query) < 2:
        return

    results = []
    with open('kaiku.json', 'r') as file:
        accounts = json.load(file)

    for item in [x for x in accounts if query in x["name"].lower()]:
        description = item["instances"][-1]["code"]
        summary = f"*{(item['name'])}*\n\n"
        for thing in item["instances"]:
            summary += f"*{thing['year']}*\n"
            summary += f"Code: {thing['code']}\n"
            if "letter" in thing.keys():
                summary += f"Grade: {thing['letter']} ({str(thing['grade'])})\n"
            else:
                summary += f"Grade: ({str(thing['grade'])})\n"
            summary += f"Sample Size: {str(thing['sampleSize'])}\n\n"

        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title=item["name"],
            description=description,
            input_message_content=InputTextMessageContent(
                summary,
                parse_mode=ParseMode.MARKDOWN
            )))

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(str(os.environ['TOKEN']), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("hertsi", menu.hertsi))
    dp.add_handler(CommandHandler("newton", menu.newton))
    dp.add_handler(CommandHandler("reaktori", menu.reaktori))
    dp.add_handler(CommandHandler("menu", menu.menu))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(evaluation.conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
