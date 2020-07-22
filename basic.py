import General
import ClassDB
from telegram import ReplyKeyboardMarkup


def start_conversation(update, context):
    """Start the conversation for the first time with the bot."""
    try:
        cid = update.message.chat_id

        # create user in database if not existing
        if cid not in ClassDB.actual_users:
            # store the user obj in users
            u = ClassDB.User(cid)
            ClassDB.actual_users[cid] = u
            ClassDB.actual_db.add_user(u)

        reply_text = 'Hello my friend! here is the menu!\n\n'
        # reply_text += ClassDB.sprint_cmd_list(General.menu_cmd_list)
        markup = General.markup_menu
        update.message.reply_text(reply_text, reply_markup=markup)

        return General.MENU

    except Exception as E:
        print(E)


def use_custom_keyb(update, context):
    """Start the conversation for the first time with the bot."""
    try:
        text = 'HEY!!! Come on, pls user the custom keyboard. My ' \
               'master invested a lot of time for this and he does ' \
               'not want STUPID PEOPLE TO RUIN EVERYTHING HE EVER ' \
               'WANTED IN LIFE!!\n\nI am sorry. I should not shout. ' \
               'I am just a bot. '
        update.message.reply_text(text)

    except Exception as E:
        print(E)


def default(update, context):
    reply_text = 'default triggered!'
    reply_markup = ReplyKeyboardMarkup([["/start"]],
                                       one_time_keyboard=True)
    update.message.reply_text(reply_text, reply_markup=reply_markup)


def fallback(update, context):
    reply_text = 'something doesnt quite fit, you should try again.'
    update.message.reply_text(reply_text)
    return General.MENU