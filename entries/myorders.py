from lib import deco
from lib.database import db
from emoji import emojize
from pprint import pprint

@deco.restricted
@deco.conversation_command_handler("myorders", pass_user_data=True)
def myorders(update, context):
    chat_id = update.effective_message.chat_id
    #user_id = context.user_data['user_id']
    #username = context.user_data['username']
    user_id = update.message.from_user.id
    username = update.message.from_user.username   
    
    update.message.reply_text(user_id)
    result = db.completed.find({})
    val = ""
    orders_msg = emojize( " <b> שלום {} להלן רשימת ההזמנות שביצעתם: </b>\n\n".format(username))
    update.message.reply_text(orders_msg, parse_mode='HTML')
    
    for user in result:

        if user_id == user["UserId"]:
            user_order_details = pprint(user)
            msg = str(user_order_details) + "\n ################" + "\n"
            update.message.reply_text(msg, parse_mode='HTML')
        else:
            pass
    update.message.reply_text("לא נמצאו רשומות בהמתנה!")
