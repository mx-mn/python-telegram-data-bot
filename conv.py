
# to write:
# update.message.reply_text(reply_text, reply_markup=reply_markup)
# to read :
# msg = update.message.text

from users import Question, User

MENU, MINING, ADD1, ADD2, ADD3, ADD4 = range(6)

cmd_mining = 'mining'
cmd_add = 'add'
cmd_edit = 'edit'
cmd_timer = 'timer'
cmd_keyboard_finished = 'finished'
cmd_next_row = 'next_row'
cmd_prev_col = 'prev_col'
cmd_prev_row = 'prev_row'
cmd_start = 'start'

menu_cmd_list = [cmd_mining, cmd_add, cmd_edit, cmd_timer]


all_keyboards = ['normal', 'new custom keyboard']

test_user = User()


def sprint_cmd_list(cmd_list):
    """Returns column of clickable commands from list."""
    ret = ''
    for cmd in cmd_list:
        ret += '/' + cmd + '\n'
    return ret


def get_current_user(update):
    """Returns the user object of the current update."""
    return test_user


def cmd_start_func(update, context):
    """Start the conversation for the first time with the bot."""
    reply_text = 'Hello my friend! here is the menu!\n\n'
    reply_text += sprint_cmd_list(menu_cmd_list)
    update.message.reply_text(reply_text)

    return MENU
