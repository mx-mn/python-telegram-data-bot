
# to write:
# update.message.reply_text(reply_text, reply_markup=reply_markup)
# to read :
# msg = update.message.text

from users import Question, User
from telegram import ReplyKeyboardMarkup

MENU, MINING, ADD1, ADD2, ADD3, ADD4 = range(6)


cmd_mining = 'mining'
cmd_add = 'add'
cmd_edit = 'edit'
cmd_timer = 'timer'
cmd_keyboard_finished = 'stop'
cmd_next_row = 'next_row'
cmd_next_col = 'next_col'
cmd_start = 'start'

menu_cmds = [cmd_mining, cmd_add, cmd_edit, cmd_timer]
create_keyboard_cmds = [cmd_next_col, cmd_next_row, cmd_keyboard_finished]


def sprint_cmd_list(cmd_list):
    ret = ''
    for cmd in cmd_list:
        ret += '/' + cmd + '\n'
    return ret


all_keyboards = ['normal', 'new custom keyboard']

latest_question = "new_question"

test_user = User()
registered_users = {}


def get_current_user(update):
    return test_user


def cmd_add_func(update, context):

    reply_text = 'Type the Question you want to ask yourself!'
    update.message.reply_text(reply_text)

    return ADD1


def add1_receive_question_text(update, context):
    new_question = Question()
    new_question.text = update.message.text
    context.chat_data[latest_question] = new_question

    reply_text = 'Choose a Keyboard or create a new one'
    reply_markup = ReplyKeyboardMarkup.from_row(all_keyboards)
    update.message.reply_text(reply_text, reply_markup=reply_markup)

    return ADD2


def add2_use_normal_keyboard(update, context):

    new_question = context.chat_data[latest_question]
    new_question.custom = False

    return add3_keyboard_finished(update, context)


def add2_create_custom_keyboard(update, context):

    new_question = context.chat_data[latest_question]
    new_question.custom = True

    context.chat_data["row"] = 0
    context.chat_data["col"] = 0

    reply_text = sprint_cmd_list(create_keyboard_cmds)
    update.message.reply_text(reply_text)

    return ADD3


def add3_next_row(update, context):
    context.chat_data["row"] += 1


def add3_next_col(update, context):
    context.chat_data["col"] += 1


def add3_set_key(update, context):

    new_question = context.chat_data[latest_question]
    row = context.chat_data["row"]
    col = context.chat_data["col"]

    new_question.keyboard[col][row] = update.message.text
    context.chat_data["col"] += 1


def add3_keyboard_finished(update, context):

    new_question = context.chat_data[latest_question]
    get_current_user(update).add_question(new_question)

    reply_text = "Great, I like it!"
    update.message.reply_text(reply_text)

    return MENU


def cmd_start_func(update, context):
    """Start the conversation for the first time with the bot."""
    reply_text = 'Hello my friend! here is the menu!\n\n'
    reply_text += sprint_cmd_list(menu_cmds)
    update.message.reply_text(reply_text)

    return MENU
