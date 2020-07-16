from telegram import ReplyKeyboardMarkup
import conv


def start(update, context):
    """Start the data collection process with user."""
    user = conv.get_current_user(update)
    user.question_counter = 0
    return collect(update, context)


def collect(update, context):
    """Store the response and ask the next question.

    First, if there was a previous question, the result is stored in
    user-class. Then if there is a next question it will be asked.
    otherwise, will return to MENU.
    """
    user = conv.get_current_user(update)

    if user.question_counter != 0:
        user.store_response(update.message.text)

    try:
        question = user.get_next_question()
    except:
        user.upload_responses_to_database()
        update.message.reply_text('No Questions left to answer')
        return conv.MENU
    else:
        reply_text = question.text
        markup = question.get_markup()

        update.message.reply_text(reply_text, reply_markup=markup)
        user.question_counter += 1
        return conv.MINING
