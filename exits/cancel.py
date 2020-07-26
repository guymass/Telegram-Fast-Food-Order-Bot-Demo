from lib import deco
from lib.database import db
from time import sleep
from entries.welcome import welcome

@deco.run_async
@deco.register_state_callback("cancel", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
@deco.fallback_handler(pattern="^cancel$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def cancel(update, context):
    query = update.callback_query
    query.answer()
    
    username = query.from_user.username
    CartId = context.user_data['CartId']
    user_id = context.user_data['user_id']
    #print("CART ID >>>>>>>>>>>>>>>>>> " + str(cart_id))
    if username == None:
        firstName = query.from_user.first_name
        lastName = query.from_user.last_name
        username = str(firstName) + " " +  str(lastName)
    query.edit_message_text("להתראות {}".format(username))
    chat_id = update.effective_message.chat_id
    cursor = db.messages.find({})

    for m in cursor:
        print(m)
        if m !=0:

            msgId = m["MessageId"]
            if msgId == 0:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - >>>>>>>>>>הודעה ריקה - אין ID")
                pass
            else:
                try:
                    context.bot.delete_message(chat_id, msgId)
                except:
                    print(str(msgId) + "<<<< הודעה אינה קיימת!")
                    pass
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - >>>>>>>>>> אין הודעות")
            pass
    start_message_id = context.user_data['start_message_id']
    start_message_id = start_message_id - 20

    msg_id_range = start_message_id+40
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
    print("ההודעות והעגלה נמחקו!\n")
    sleep(1)
    welcome(update, context)
