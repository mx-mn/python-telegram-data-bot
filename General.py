from ClassDB import Database, User, Question


def get_user(chat_id):
    """Returns the user object of the current update."""
    global actual_users
    u = actual_users[chat_id]
    return u


def set_user(user):
    """Inserts user if not existing, otherwise overrides existing."""
    global actual_users
    actual_users[user.chat_id] = user


def cmd_start_func(update, context):
    """Start the conversation for the first time with the bot."""

    cid = update.message.chat_id

    # create user in database if not existing
    if cid not in actual_users:
        # store the user obj in users
        u = User(cid)
        actual_users[cid] = u
        actual_db.add_user(u)

    reply_text = 'Hello my friend! here is the menu!\n\n'
    reply_text += sprint_cmd_list(menu_cmd_list)
    update.message.reply_text(reply_text)

    return MENU


def sprint_cmd_list(cmd_list):
    """Returns column of click-able commands from list."""
    ret = ''
    for cmd in cmd_list:
        ret += '/' + cmd + '\n'
    return ret


global actual_users
global actual_db

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


def init():
    global actual_users
    global actual_db

    actual_db = Database(
        "mongodb+srv://MASTER:9NZc9agZd21YP9nL@cluster0.umetu"
        ".azure.mongodb.net/mydatabase?retryWrites=true&w"
        "=majority", "mydatabase", "python_telegram_bot")
    actual_users = actual_db.get_all_users()


def test():
    init()


# test()
