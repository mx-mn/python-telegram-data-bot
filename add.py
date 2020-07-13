import conv
from telegram import ReplyKeyboardMarkup

latest_question = "new_question"
create_keyb_cmd_list = [conv.cmd_prev_col,
                        conv.cmd_prev_row,
                        conv.cmd_next_row,
                        conv.cmd_keyboard_finished]


def start(update, context):
    reply_text = 'Type the Question you want to ask yourself!'
    update.message.reply_text(reply_text)

    return conv.ADD1


def question_text_defined(update, context):
    new_question = conv.Question()
    new_question.text = update.message.text
    context.chat_data[latest_question] = new_question

    reply_text = 'Choose a Keyboard or create a new one'
    reply_markup = ReplyKeyboardMarkup.from_row(conv.all_keyboards)
    update.message.reply_text(reply_text, reply_markup=reply_markup)

    return conv.ADD2


def std_keyb_used(update, context):
    new_question = context.chat_data[latest_question]
    new_question.custom = False

    return keyb_done(update, context)


def use_custom_keyb(update, context):
    new_question = context.chat_data[latest_question]
    new_question.custom = True

    context.chat_data["row"] = 0
    context.chat_data["col"] = 0

    # TODO: add desc of what to do next to reply_text
    reply_text = conv.sprint_cmd_list(create_keyb_cmd_list)
    update.message.reply_text(reply_text)

    return conv.ADD3


def next_row(update, context):
    """Increase the row, append one if necessary."""
    new_question = context.chat_data[latest_question]
    row = context.chat_data["row"] + 1
    context.chat_data["col"] = 0

    # append row when index exceeded
    if row == len(new_question.keyboard):
        new_question.keyboard.append([])

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
    new_question = context.chat_data[latest_question]
    row = context.chat_data["row"]
    col = context.chat_data["col"]

    new_question.keyboard[row].insert(col, update.message.text)
    next_col(update, context)

    reply_text = sprint_keyboard(update, context) + '\n' + \
                 conv.sprint_cmd_list(create_keyb_cmd_list)
    update.message.reply_text(reply_text)


def keyb_done(update, context):
    new_question = context.chat_data[latest_question]
    conv.get_current_user(update).add_question(new_question)

    reply_text = "Great, I like it!" + '\n' \
                 + conv.sprint_cmd_list(conv.menu_cmd_list)
    update.message.reply_text(reply_text)

    return conv.MENU


def sprint_keyboard(update, context):
    """Returns multi-line string of current keyboard."""
    new_question = context.chat_data[latest_question]
    ret = ''
    for row in new_question.keyboard:
        for key in row:
            ret += '[' + key + '] '
        ret += '\n'
    return ret
