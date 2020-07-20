from telegram import ReplyKeyboardMarkup
import General


def start(update, context):
    """Start the data collection process with user."""
    cid = update.message.chat_id
    user = General.get_user(cid)
    user.next_question = 0
    General.set_user(user)
    return collect(update, context)


def collect(update, context):
    """Store the response and ask the next question.

    First, if there was a previous question, the result is stored in
    user-class. Then if there is a next question it will be asked.
    otherwise, will return to MENU.
    """
    cid = update.message.chat_id
    user = General.get_user(cid)

    if user.next_question > 0:
        user.store_prev_question_response(update.message.text)

    try:
        question = user.get_next_question()
    except:
        update.message.reply_text('No Questions left to answer')
        return General.MENU
    else:
        reply_text = question.text
        markup = question.get_markup()
        update.message.reply_text(reply_text, reply_markup=markup)
        return General.MINING
