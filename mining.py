import conversation


def start(update, context):
    """Start the data collection process with user."""
    user = conversation.get_current_user(update)
    update.message.reply_text('great. let us start mining')
    user.question_counter = 0
    return mining(update, context)


def mining(update, context):
    """Store the response and ask the next question.

    First, if there was a previous question, the result is stored in
    user-class. Then if there is a next question it will be asked.
    otherwise, will return to MENU.
    """
    user = conversation.get_current_user(update)
    if user.question_counter != 0:
        user.store_response(update.message.text)

    try:
        question = user.get_next_question()
    except:
        return conversation.MENU
    else:
        update.message.reply_text(question.text)
        user.question_counter += 1
        return conversation.MINING
