from lib import deco
from lib.database import db
from time import sleep
from settings import CHATID

@deco.run_async
@deco.restricted
@deco.conversation_command_handler("products")
def products(update, context):
    products = db.images.find({})
    update.message.reply_text(" אלו הם המוצרים הזמינים לבוט.\n\n")
    for prd in products:
        imageId = prd['ImageId']
        msg = prd['ImageText']
        if prd['FileType'] == "video/mp4" or prd['FileType'] == "video":
            context.bot.send_video(CHATID, video=imageId, caption=msg, parse_mode='HTML')
            sleep(1)
        elif prd['FileType'] == "document":
            context.bot.send_document(CHATID, document=imageId, caption=msg, parse_mode='HTML')
            sleep(1)
        elif prd['FileType'] == "photo":
            context.bot.send_photo(CHATID, imageId, msg, parse_mode='HTML')
            sleep(1)
