import logging

from telegram import (Chat, ChatAction, ChatMember, Message, MessageEntity, ParseMode)
from telegram.ext import (Defaults, Updater, ConversationHandler)
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
                          Filters)
from lib import deco, utils
from settings import CHATID, token, timeout
from persistence import init_persistance

from entries import *
from states import *
from exits import cancel
from time import sleep

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@deco.run_async
def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    print("\n------------------------------------------------------------\nStarting bot")
    persistance = init_persistance()
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(token, persistence=persistance, use_context=True, defaults=defaults,
                    request_kwargs={'read_timeout': timeout, 'connect_timeout': timeout})
    job_queue = updater.job_queue

    SELF_CHAT_ID = f'@{updater.bot.get_me().username}'
    logger.info(f'SELF_CHAT_ID {SELF_CHAT_ID}')
    logger.info(f'CHATID {CHATID}')

    conversation_handler = ConversationHandler(
        entry_points=deco.entry_points,
        states=deco.entry_states,
        fallbacks=deco.entry_fallbacks,
        name="order",
        persistent=True,
        allow_reentry=True,
        per_user=True,
        per_chat=True,
        # per_message=True
    )

    updater.dispatcher.add_handler(conversation_handler)

    for dispather in deco.global_dispatchers:
        updater.dispatcher.add_handler(dispather)

    #updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    print("Started polling...")
    updater.idle()


if __name__ == '__main__':
    main()
