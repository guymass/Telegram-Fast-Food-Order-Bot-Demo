from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from settings import CHATID
from time import sleep
from entries.welcome import welcome

@deco.run_async
@deco.fallback_handler(pattern="^cb_end$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def end(update, context):
    query = update.callback_query
    data = update.callback_query.data
    user_data = context.user_data

    username = query.from_user.username
    CartId = context.user_data['CartId']
    user_id = context.user_data['user_id']
    if username == None:
        username = user_data['username']
    query.edit_message_text("Goodbye {}".format(username))
    chat_id = CHATID

    cursor = db.messages.find({})
    for m in cursor:

        if m !=0:

            msgId = m["MessageId"]
            if msgId == 0:
                
                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                except:
                    print(str(msgId) + "Message does not exist!")
                    pass
        else:
            print("No Messages")
            pass
    start_message_id = context.user_data['start_message_id']
    start_message_id = start_message_id - 20

    msg_id_range = start_message_id+20
    for i in range(start_message_id, msg_id_range):

        try:
            context.bot.delete_message(chat_id, i)
            print('Message {} Deleted'.format(i))
            i += 1
        except:
            print("NO Message ID {} Found, not deleted".format(i))
    x = db.messages.delete_many({})
    y = db.tmp_orders.delete_many({})
    

    resdel = db.cart.delete_many({'UserOrderId': user_id})
    print("MEssages and UserCart deleted! \n")
    sleep(1)
    welcome(update, context)
