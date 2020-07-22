from telegram import ReplyKeyboardMarkup
import General
import ClassDB


def start(update, context):
    """Start the data collection process with user."""
    cid = update.message.chat_id
    user = ClassDB.get_user(cid)
    user.next_question = 0
    ClassDB.set_user(user)
    return collect(update, context)


def collect(update, context):
    """Store the response and ask the next question.

    First, if there was a previous question, the result is stored in
    user-class. Then if there is a next question it will be asked.
    otherwise, will return to MENU.
    """
    try:
        cid = update.message.chat_id
        user = ClassDB.get_user(cid)

        if user.next_question > 0:
            user.store_prev_question_response(update.message.text)

        question = user.get_next_question()

    except:
        cid = update.message.chat_id
        user = ClassDB.get_user(cid)
        text = 'You are done! Congrats for another successful ' \
               'day!'
        markup = General.markup_menu
        update.message.reply_text(text, reply_markup=markup)
        return General.MENU
    else:
        reply_text = question.text
        markup = question.get_markup()
        update.message.reply_text(reply_text, reply_markup=markup)
        return General.MINING
