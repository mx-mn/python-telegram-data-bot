from telegram import ReplyKeyboardMarkup

MENU, MINING, ADD1, ADD2, ADD3, ADD4, TIMER1, TIMER2 = \
    range(8)

cmd_mining = 'check_in'
cmd_add = 'add'
cmd_edit = 'edit'
cmd_timer = 'timer'
cmd_keyboard_finished = 'done'
cmd_next_row = 'next_row'
cmd_prev_col = 'previous_column'
cmd_prev_row = 'previous_row'
cmd_start = 'start'
cmd_stop_timer = 'disable'

menu_cmd_list = [cmd_mining, cmd_add, cmd_edit, cmd_timer]

stop_timer = 'stop'
delay5 = '5minutes'
delay60 = '1hour'
delay180 = '3hours'
delay_today = 'tomorrow'

markup_timer = ReplyKeyboardMarkup(
    [['/' + cmd_mining], ['/' + delay5],
     ['/' + delay60],
     ['/' + delay180],
     ['/' + delay_today]],
    one_time_keyboard=True)

markup_menu = ReplyKeyboardMarkup(
    [['/' + cmd_mining],
     ['/' + cmd_add,
      '/' + cmd_timer,
      '/' + cmd_edit]],
    one_time_keyboard=True)

normal = 'normal'
new_custom = 'new custom keyboard'

markup_keyboard_overview = ReplyKeyboardMarkup(
    [[normal,
      new_custom]],
    one_time_keyboard=True)
