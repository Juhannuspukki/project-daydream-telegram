import json
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, MessageHandler, Filters, ConversationHandler)


COURSENAME, COURSEYEAR, USEFULNESS, ARRANGEMENTS, LEARNING, EVALUATION, RECOMMENDATION, THANKS = range(8)


def ratecourse(update, context):
    update.message.reply_text(
        "Hello! Please tell me the name of the course you would like to rate.\n\nPlease note that your answers won't "
        "be saved. This program is only a prototype for evaluating the viability of rating courses via Telegram. You "
        "can write /cancel to cancel the questionnaire at any time.")
    return COURSENAME


def course_name(update, context):
    course_search_string = update.message.text.lower()

    with open('kaiku.json', 'r') as file:
        accounts = json.load(file)

    reply_keyboard = []
    if len(course_search_string) > 3:
        for item in [x for x in accounts if course_search_string in x["name"].lower()]:
            reply_keyboard.append([item["name"]])
            if len(reply_keyboard) > 10:
                break

        if len(reply_keyboard) == 0:
            update.message.reply_text('There are no courses by that name. /ratecourse')
            return ConversationHandler.END

        update.message.reply_text('The following courses were found:',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return COURSEYEAR

    else:
        update.message.reply_text('Please enter at least 4 characters. /ratecourse')
        return ConversationHandler.END


def course_year(update, context):
    course_search_string = update.message.text.lower()

    with open('kaiku.json', 'r') as file:
        accounts = json.load(file)

    reply_keyboard = []
    for item in [x for x in accounts if course_search_string == x["name"].lower()]:
        for thing in item["instances"]:
            reply_keyboard.append([thing["year"]])

    if len(reply_keyboard) == 0:
        update.message.reply_text('That course does not appear to exist. /ratecourse')
        return ConversationHandler.END

    update.message.reply_text('When was the course in question held?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return USEFULNESS


def usefulness(update, context):
    reply_keyboard = [["0", "1", "2", "3", "4", "5"], ["I choose not to answer"]]
    update.message.reply_text("How much do you agree with the following statements on a scale from 0 to 5? 0 == not at "
                              "all, 5 == completely agree\n\nThe course covered topics that I found useful and/or "
                              "relevant.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ARRANGEMENTS


def arrangements(update, context):
    reply_keyboard = [["0", "1", "2", "3", "4", "5"], ["I choose not to answer"]]
    update.message.reply_text("Course personnel communicated clearly and the schedules were sensible.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LEARNING


def learning(update, context):
    reply_keyboard = [["0", "1", "2", "3", "4", "5"], ["I choose not to answer"]]
    update.message.reply_text("I learned a lot on the course.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return EVALUATION


def evaluation(update, context):
    reply_keyboard = [["0", "1", "2", "3", "4", "5"], ["I choose not to answer"]]
    update.message.reply_text("The grade I received accurately describes my knowledge of the course's topics.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return RECOMMENDATION


def recommendation(update, context):
    reply_keyboard = [["0", "1", "2", "3", "4", "5"], ["I choose not to answer"]]
    update.message.reply_text("I would recommend this course.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return THANKS


def thanks(update, context):
    update.message.reply_text('Thank you for evaluating this course!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('ratecourse', ratecourse)],

        states={
            COURSENAME: [MessageHandler(Filters.text, course_name)],

            COURSEYEAR: [MessageHandler(Filters.text, course_year)],

            USEFULNESS: [MessageHandler(Filters.text, usefulness)],

            ARRANGEMENTS: [MessageHandler(Filters.text, arrangements)],

            LEARNING: [MessageHandler(Filters.text, learning)],

            EVALUATION: [MessageHandler(Filters.text, evaluation)],

            RECOMMENDATION: [MessageHandler(Filters.text, recommendation)],

            THANKS: [MessageHandler(Filters.text, thanks)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
