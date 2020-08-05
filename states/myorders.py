from lib import deco, states
from lib.database import db
from emoji import emojize
from pprint import pprint
from time import sleep

@deco.restricted
@deco.register_state_callback(states.FIRST, pattern='^cb_myorders$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def myorders(update, context):
    chat_id = update.effective_message.chat_id
    user_id = context.user_data['user_id']
    order_id = context.user_data['CartId']

    result = db.completed.find({})
    val = ""
   
    # Initialize some vars
    msg = ""
    username = ""
    for user in result:
        
        if user_id == user["UserId"]:
            username = user['UserName']
            for keys in user.keys(): 

                msg += " \U000025AA" + str(keys) + " : " + str(user[keys]) + "\U000025AA\n"

    orders_msg = emojize( " <b>Hello {}, here are a list of your orders:</b>\n\n".format(username))
    context.bot.send_message(chat_id, orders_msg)
    msgs = [msg[i:i + 2048] for i in range(0, len(msg), 2048)]
    message = ""
    for text in msgs:
        
        message += "  \U0001F4A2  \U0001F4A2  \U0001F4A2  \U0001F4A2  \U0001F4A2 \n\n" + str(text) + "\n\n \U0001F4A2  \U0001F4A2  \U0001F4A2  \U0001F4A2  \U0001F4A2"
        context.bot.send_message(chat_id, message)
        sleep(1)
