from lib import deco
from lib.database import db
from emoji import emojize

@deco.restricted
@deco.conversation_command_handler("getlist")
def getlist(update, context):
    result = db.completed_orders.find({})
    val = ""
    for r in result:

        if r["Status"] == "Waiting":
            msg = emojize( "\U0000200F :mailbox:<b> הזמנה בהמתנה:</b>\n\n" + str(r["Status"]) + " מצב הזמנה :exclamation:" + "\n" + str(r["Mobile"]) + " - :iphone: " + "\n" + str(r["Address"] )+ " - :truck: " + "\n" + str(r["Product"]) + ":package: " , use_aliases=True)
            msg += emojize("\n" + str(r["Quantity"]) + " \U00002B05\n\U00002139 " + str(r["Message"]) + " \U00002139\n ", use_aliases=True)
            update.message.reply_text(msg, parse_mode='HTML')

        elif r["Status"] == '' or r["Status"] == 'Delivered':
            pass
        else:
            update.message.reply_text("לא נמצאו רשומות בהמתנה!")
