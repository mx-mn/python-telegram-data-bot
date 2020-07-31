from telegram.ext import Updater, ConversationHandler, CommandHandler, \
    MessageHandler, Filters
import General
import basic
import mining
import add
import timer
import ClassDB
import credentials


def main():
    updater = Updater(credentials.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue
    job_queue.set_dispatcher(dispatcher)

    ClassDB.init(credentials.connection_string, credentials.database_name,
                 credentials.collection_name)

    conversation_handler = ConversationHandler(

        # A list of Handler objects that can trigger
        # the start of the conversation.
        # Type:	List[telegram.ext.Handler]
        entry_points=[
            CommandHandler(General.cmd_start,
                           basic.start_conversation),
            MessageHandler(Filters.all, basic.default)],

        # A dict that defines the different states of conversation
        # a user can be in and one or more associated Handler
        # objects that should be used in that state.
        # Type:	Dict[object, List[telegram.ext.Handler]]
        states=
        {
            General.MENU:
                [
                    CommandHandler(General.cmd_mining,
                                   mining.start),
                    CommandHandler(General.cmd_add,
                                   add.start),
                    CommandHandler(General.cmd_edit,
                                   basic.default),
                    CommandHandler(General.cmd_timer,
                                   timer.start),
                    CommandHandler(General.delay5, timer.delay5),
                    CommandHandler(General.delay60, timer.delay60),
                    CommandHandler(General.delay180, timer.delay180),
                    CommandHandler(General.delay_today,
                                   timer.delay_today),
                    MessageHandler(Filters.all,
                                   basic.use_custom_keyb),
                ],
            General.MINING:
                [
                    MessageHandler(Filters.text,
                                   mining.collect)
                ],
            General.ADD1:
                [
                    MessageHandler(Filters.text,
                                   add.question_text_defined)
                ],
            General.ADD2:
                [
                    MessageHandler(Filters.text(General.normal),
                                   add.std_keyb_used),
                    MessageHandler(Filters.text(General.new_custom),
                                   add.use_custom_keyb),
                ],
            General.ADD3:
                [
                    CommandHandler(General.cmd_next_row,
                                   add.next_row),
                    CommandHandler(General.cmd_prev_col,
                                   add.prev_col),
                    CommandHandler(General.cmd_prev_row,
                                   add.prev_row),
                    CommandHandler(General.cmd_keyboard_finished,
                                   add.done),
                    MessageHandler(Filters.text,
                                   add.set_key),
                ],
            General.TIMER1:
                [
                    CommandHandler(General.cmd_stop_timer,
                                   timer.stop),
                    MessageHandler(Filters.regex('^([0-1]?[0-9]|2['
                                                 '0-3]):[0-5]['
                                                 '0-9]$'),
                                   timer.time_valid),
                    MessageHandler(Filters.all, timer.time_invalid)
                ],
        },

        # A list of handlers that might be used if the user is in a
        # conversation, but every handler for their current
        # state returned False on check_update.
        # Type:	List[telegram.ext.Handler]
        fallbacks=[CommandHandler('cancel', basic.fallback)]
    )
    dispatcher.add_handler(conversation_handler)
    print("start polling...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
