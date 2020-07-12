from users import Question, User
from telegram import ReplyKeyboardMarkup

MENU, MINING, ADD1, ADD2, ADD3, ADD4 = range(6)

cmd_mining = '/mining'
cmd_add = '/add'
cmd_edit = '/edit'
cmd_timer = '/timer'

all_keyboards = ['normal', 'new custom keyboard']

registered_users = {}


def get_current_user(update):
    return registered_users[update.message.chat_id]


def cmd_add_func(update, context):
    update.message.reply_text()

    reply_text = 'Type the Question you want to ask yourself!'
    update.message.reply_text(reply_text)

    return ADD1


def add1_receive_question_text(update, context):
    new_question = Question()
    new_question.set_text(update.message.text)
    context.chat_data["new_question"] = new_question

    reply_text = "Choose a Keyboard or create a new one"
    reply_markup = ReplyKeyboardMarkup.from_column(all_keyboards)
    update.message.reply_text(reply_text, reply_markup)

    return ADD2


def add2_use_normal_keyboard(update, context):

    new_question = context.chat_data["new_question"]
    new_question.custom = False
    get_current_user(update).add_question(new_question)

    return MENU


def add2_create_custom_keyboard(update, context):
    return ADD3


def add2_use_custom_keyboard(update, context):

    new_question = context.chat_data["new_question"]
    new_question.custom = True
    new_question.set_keyboard()

    get_current_user(update).add_question(new_question)

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

