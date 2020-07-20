import General
from telegram import ReplyKeyboardMarkup

latest_question = "new_question"
create_keyb_cmd_list = [General.cmd_prev_col,
                        General.cmd_prev_row,
                        General.cmd_next_row,
                        General.cmd_keyboard_finished]


def start(update, context):
    reply_text = 'Type the Question you want to ask yourself!'
    update.message.reply_text(reply_text)

    return General.ADD1


def question_text_defined(update, context):
    cid = update.message.chat_id
    user = General.get_user(cid)
    user.temp_question = General.Question()
    user.temp_question.text = update.message.text

    reply_text = 'Choose a Keyboard or create a new one'
    reply_markup = ReplyKeyboardMarkup.from_row(
        General.all_keyboards, one_time_keyboard=True)
    update.message.reply_text(reply_text, reply_markup=reply_markup)

    return General.ADD2


def std_keyb_used(update, context):
    cid = update.message.chat_id
    user = General.get_user(cid)
    user.temp_question.is_custom = False

    return keyb_done(update, context)


def use_custom_keyb(update, context):
    cid = update.message.chat_id
    user = General.get_user(cid)
    user.temp_question.is_custom = True

    context.chat_data["row"] = 0
    context.chat_data["col"] = 0

    reply_text = 'You are something else! So let me explain.\nAdd a ' \
                 'button by just sending the text it should say. ' \
                 'Then you have the commands below to control the ' \
                 'process.\n'
    reply_text += General.sprint_cmd_list(create_keyb_cmd_list)
    update.message.reply_text(reply_text)

    return General.ADD3


def next_row(update, context):
    """Increase the row, append one if necessary."""
    cid = update.message.chat_id
    user = General.get_user(cid)

    row = context.chat_data["row"] + 1
    context.chat_data["col"] = 0

    # append row when index exceeded
    if row == len(user.temp_question.keyboard):
        user.temp_question.keyboard.append([])

    context.chat_data["row"] = row


def next_col(update, context):
    context.chat_data["col"] += 1


def prev_row(update, context):
    if context.chat_data["row"] > 0:
        context.chat_data["row"] -= 1
        context.chat_data["col"] = 0


def prev_col(update, context):
    if context.chat_data["col"] > 0:
        context.chat_data["col"] -= 1


def set_key(update, context):
    """Set the received msg as key, print current keyboard + cmds."""
    row = context.chat_data["row"]
    col = context.chat_data["col"]

    cid = update.message.chat_id
    user = General.get_user(cid)
    user.temp_question.keyboard[row].insert(col, update.message.text)

    next_col(update, context)

    reply_text = user.temp_question.sprint_keyboard() + '\n' + \
                 General.sprint_cmd_list(create_keyb_cmd_list)
    update.message.reply_text(reply_text)


def keyb_done(update, context):
    try:
        cid = update.message.chat_id
        user = General.get_user(cid)
        user.add_question(user.temp_question)
        reply_text = "Great, I like it!" + '\n' \
                     + General.sprint_cmd_list(General.menu_cmd_list)

        update.message.reply_text(reply_text)
        return General.MENU

    except Exception as E:
        print(E)


def sprint_keyboard(update, context):
    """Returns multi-line string of current keyboard."""
    cid = update.message.chat_id
    user = General.get_user(cid)
    new_question = user.temp_question
    ret = ''
    for row in new_question.keyboard:
        for key in row:
            ret += '[' + key + '] '
        ret += '\n'
    return ret
