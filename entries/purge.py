from lib import deco
from lib.database import db

@deco.restricted
@deco.conversation_command_handler("purge")
def purge(update, context):
    chat_id = update.effective_message.chat_id
    msg = " כל הרשומות נמחקו!"
    x = db.completed_orders.delete_many({})
    context.bot.send_message(chat_id, msg)

