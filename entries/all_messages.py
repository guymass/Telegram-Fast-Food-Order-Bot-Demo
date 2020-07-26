from telegram import MessageEntity
from telegram.ext import Filters
from lib import deco
from lib.database import db

@deco.run_async
# TODO: bot name
@deco.global_message_handler (Filters.user('@order_il_bot') and Filters.entity(MessageEntity.TEXT_LINK) and (
        Filters.entity(MessageEntity.URL)) and (Filters.text | Filters.video | Filters.photo | Filters.document))
def all_messages(update, context):

    msgId = update.message.message_id
    text = update.message.text

    item = {
        "MessageId":msgId,
        "MessageText":text
    }

    if db.messages.count_documents({'MessageId': msgId}, limit=1) > 0:
        print("הודעה רשומה כבר!")
        pass
    else:
        db.messages.insert_one(item)
        print(str(msgId) + " >>>>>>> פרטי ההודעה נשמרו! <<<<<<<<<<")
