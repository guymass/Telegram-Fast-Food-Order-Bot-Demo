from lib import deco
from lib.database import db

@deco.restricted
@deco.conversation_command_handler("clear")
def clear_images(update, context):
    chat_id = update.effective_message.chat_id
    msg = " כל התמונות נמחקו, אנא עדכנו תמונות חדשות על ידי העלאה לצאט."
    x = db.images.delete_many({})
    x = db.videos.delete_many({})
    context.bot.send_message(chat_id, msg)
