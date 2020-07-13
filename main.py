
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import conversation


def default(update, context):
    print("default triggered")
    update.message.reply_text('default triggered. returning to state: MENU')


def fallback(update, context):
    print("fallback triggered")
    update.message.reply_text('fallback triggered. returning to state: MENU')


def main():
    bot_token = "TOKEN"

    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    conversation_handler = ConversationHandler(

        # A list of Handler objects that can trigger the start of the conversation.
        # Type:	List[telegram.ext.Handler]
        entry_points=[MessageHandler(Filters.all, default)],

        # A dict that defines the different states of conversation a user can be in and one or more associated Handler
        # objects that should be used in that state. Type:	Dict[object, List[telegram.ext.Handler]]
        states=
        {
            conversation.MENU:
            [
                CommandHandler(conversation.cmd_mining, conversation.cmd_mining_func),
                CommandHandler(conversation.cmd_add, conversation.cmd_add_func),
                CommandHandler(conversation.cmd_edit, conversation.cmd_edit_func),
                CommandHandler(conversation.cmd_timer, conversation.cmd_timer_func),
                MessageHandler(Filters.all, default)
            ],
            conversation.MINING:
            [
                MessageHandler(Filters.text, conversation.mining)
            ],
            conversation.ADD1:
            [
                MessageHandler(Filters.text, conversation.add1_receive_question_text)
            ],
            conversation.ADD2:
            [
                MessageHandler(Filters.text('normal'), conversation.add2_use_normal_keyboard),
                MessageHandler(Filters.text('new custom keyboard'), conversation.add2_create_custom_keyboard),
                MessageHandler(Filters.text, conversation.add2_use_custom_keyboard)
            ]
        },

        # A list of handlers that might be used if the user is in a conversation, but every handler for their current
        # state returned False on check_update. Type:	List[telegram.ext.Handler]
        fallbacks=[CommandHandler('cancel', fallback)]
    )

    dispatcher.add_handler(conversation_handler)
    print("start polling...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
