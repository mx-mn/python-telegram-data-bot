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


all_keyboards = ['normal', 'new custom keyboard']

latest_question = "new_question"

test_user = User()
registered_users = {}


def get_current_user(update):
    return test_user


def cmd_add_func(update, context):
    update.message.reply_text()

    reply_text = 'Type the Question you want to ask yourself!'
    update.message.reply_text(reply_text)

    return ADD1


def add1_receive_question_text(update, context):
    new_question = Question()
    new_question.text = update.message.text
    context.chat_data[latest_question] = new_question

    reply_text = "Choose a Keyboard or create a new one"
    reply_markup = ReplyKeyboardMarkup.from_column(all_keyboards)
    update.message.reply_text(reply_text, reply_markup)

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

    reply_text = cmd_next_row + '\n' + cmd_next_col + '\n' + cmd_keyboard_finished
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


def cmd_mining_func(update, context):
    user = get_current_user(update)

    update.message.reply_text('great. let us start mining')
    user.currentQuestion = 0

    # start the data mining process
    return mining(update, context)


def mining(update, context):
    user = registered_users[update.message.chat_id]
    question = user.get_next_question()

    if question == False:
        return MENU

    else:
        update.message.reply_text('next question')
        user.currentQuestion += 1
        return MINING


