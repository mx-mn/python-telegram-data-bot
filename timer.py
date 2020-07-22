import General
import ClassDB
from datetime import time, tzinfo, timedelta
import pytz
from telegram import ReplyKeyboardMarkup


def start(update, context):
    """Starting point of the timer conversation."""
    try:
        cid = update.message.chat_id
        user = ClassDB.get_user(cid)

        text = "Ready to set a timer eh? lets do it.\nEither send " \
               "the time when you want to be notified to set the " \
               "timer or press\n\n" + '/' + General.cmd_stop_timer + \
               "\n\nto disable it.\n\nSend me the time in HH:MM so " \
               "that I can understand.\n\nlike this: 04:20\n\nOh " \
               "and before I forget. I only know the UTC timezone, " \
               "because everything else makes my head hurt. So here " \
               "a little help for you to deal with this " \
               "bullshit:\n\nSummer: AUT = 14:00; UTC = " \
               "12:00\nWinter: AUT = 13:00; UTC = 12:00."
        update.message.reply_text(text)

        return General.TIMER1

    except Exception as E:
        print(E)


def stop(update, context):
    """Stops the timer_job of current user if existing."""
    try:
        cid = update.message.chat_id
        user = ClassDB.get_user(cid)

        if user.timer_job is not None:
            user.timer_job.schedule_removal()
            text = "Ok. I removed the timer. You have to create one " \
                   "again, otherwise, you will forget it all the " \
                   "time!"
        else:
            text = "Wow. You funny human dont even have a timer. " \
                   "Sometimes I am laughing at how bad you are at " \
                   "remembering stuff."

        markup = General.markup_menu
        update.message.reply_text(text, reply_markup=markup)

        return General.MENU

    except Exception as E:
        print(E)


def time_valid(update, context):
    try:
        cid = update.message.chat_id
        user = ClassDB.get_user(cid)

        utc_time = get_time(update.message.text)
        user.set_notify_time(utc_time)

        user.timer_job = context.job_queue.run_daily(
            callback=send_reminder, time=utc_time, context=cid)

        text = "time valid! So I will text you everyday at " + \
               str(utc_time) + " (UTC)"
        update.message.reply_text(text)
        return General.MENU

    except Exception as E:
        print(E)


def time_invalid(update, context):
    try:
        text = "time invalid! the format is HH:MM\nfor example " \
               "19:55. Really just 5 things. the two digits that " \
               "represent the hours, a colon (aka DoubleDot :) and " \
               "the two digits that represent the minutes.\n\nYou " \
               "got this! I believe in you, you strange biological " \
               "creature.\n\nOr just say /" + General.cmd_stop_timer
        update.message.reply_text(text)

        return General.TIMER1

    except Exception as E:
        print(E)


def get_time(msg: str) -> time:
    """Returns datetime.time obj  of HH:MM"""
    try:
        hh = msg[:2]  # first two
        mm = msg[3:]  # last two
        utc_time = time(hour=int(hh), minute=int(mm), tzinfo=pytz.utc)
        return utc_time

    except Exception as E:
        print(E)


def send_reminder(context):
    reply_text = 'time for your check in!'
    reply_markup = General.markup_timer
    context.bot.send_message(chat_id=context.job.context,
                             text=reply_text,
                             reply_markup=reply_markup)


def delay(update, context, seconds):
    cid = update.message.chat_id
    user = ClassDB.get_user(cid)
    context.job_queue.run_once(send_reminder, seconds, context=cid)


def delay5(update, context):
    sec = 5 * 60
    delay(update, context, sec)


def delay60(update, context):
    sec = 60 * 60
    delay(update, context, sec)


def delay180(update, context):
    sec = 180 * 60
    delay(update, context, sec)


def delay_today(update, context):
    pass
