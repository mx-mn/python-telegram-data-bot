from telegram import ReplyKeyboardMarkup
import Bot


def start(update, context):
    """Start the data collection process with user."""
    user = Bot.get_current_user(update, context)
    user.next_question = 0
    Bot.set_current_user(update, context, user)
    return collect(update, context)


def collect(update, context):
    """Store the response and ask the next question.

    First, if there was a previous question, the result is stored in
    user-class. Then if there is a next question it will be asked.
    otherwise, will return to MENU.
    """
    user = Bot.get_current_user(update, context)

    if user.next_question > 0:
        user.store_response(update.message.text)

    try:
        question = user.get_next_question()
    except:
        # user.upload_responses_to_database()
        update.message.reply_text('No Questions left to answer')
        return Bot.MENU
    else:
        reply_text = question.text
        markup = question.get_markup()
        update.message.reply_text(reply_text, reply_markup=markup)
        # return conv.MINING # is redundant
