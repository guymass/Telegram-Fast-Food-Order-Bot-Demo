from lib import (common, deco, states, utils)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

chosen1=[]
message=None
options1=["Salad", "Coke", "Extra ham", "Coffee", "cheese"]

def default_poll():
    return utils.multi_selection_widget(checked_symbol="✅", unchecked_symbol="☑️")

def delete_msg():
    global message
    try:
        if not message is None:
            message.delete()
    except:
        pass    

#You can create a poll to use globally just changing what you need via attributes
poll_widget=default_poll()

@deco.run_async
@deco.register_state_callback("newpoll")
def repeat_poll(update, context):
    print("Repeating polls")
    poll(update, context)

@deco.conversation_command_handler("poll")
def poll(update, context):
    global poll_widget
    poll_widget.options=options1
    poll_widget.chosen=[]  #This is being set here to clear the poll when the again button is pressed
    poll_widget.n_columns=2
    poll_widget.single_option=False
    poll_widget.payload_key="poll1",
    poll_widget.question="Choose an extra: "

    #This will set a function on the scope to be called on the callback
    poll_widget.callback=callback_func

    #Everything is setup and sent with this method call
    poll_widget.send(update, context)


#Don't worry! This function is just for showinghow you can add extra functionality as you will see below
#Go read the next function first
@deco.run_async
@deco.register_state_callback("confirm_poll_2")
def end_poll(update, context):
    global poll_widget2, message
    if len(poll_widget2.chosen)>0:
        #We can end if one thing was chosen!
        poll_widget2.end() #or finalize()

        delete_msg()
        poll_widget3=default_poll()
        poll_widget3.callback_data="pollc" #lets set this state callback
        poll_widget3.options=["Yes", "No"]
        poll_widget3.question="Are you sure?"
        poll_widget3.single_option=True
        poll_widget3.chosen=[]             #If you don't do this it will be marked with the last values
        poll_widget3.send(update, context)

    else:
        #Delete and send the message again
        delete_msg()
        message=context.bot.send_message(chat_id=update.effective_chat.id, text="Please select at least one option!")

#When using a callback function with the callback=, the first argumentwill be the poll widget
def callback_func(poll_w, update, context):
    global chosen1, poll_widget2 
    print("From callback function: ", poll_w.answer)
    chosen1=poll_w.chosen
    answers=poll_w.answer

    #Lets create another poll. You can always create a poll and pass your 
    # preferred arguments to it
    #Callback_data will call a state callback like if it was a button
    poll_widget2=utils.multi_selection_widget(
        ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"], 
        single_option=True,  #For this one only one option is accepted
        chosen=[],
        autoremove=True,    #Just to show that this option exists and it's defaulted to True
        add_confirm_button=False, #Do not add the default confirm button because we are doing this differently
        spacing=15,          #Let's add more spacing between the symbols and text
        payload_key="poll2",
        extra_buttons=[
            InlineKeyboardButton("End", callback_data="confirm_poll_2"), InlineKeyboardButton("Back", callback_data="poll_back")
            ]
    )

    #Finally send the message again
    poll_widget2.send(update, context)

@deco.run_async
@deco.register_state_callback("poll_back")
def poll_back(update, context):
    #let's just reuse poll1
    global poll_widget, poll_widget2
    delete_msg()
    poll_widget2.finalize() #Force deletes the current poll
    poll_widget.send(update, context)  #Send poll 1 again


@deco.run_async
@deco.register_state_callback("pollc")
def poll2(update, context):
    global poll_widget, poll_widget2, message
    
    #last_multi_sel is the default key for the poll data and it will overwrite by
    #default. You can change this by setting another string on the payload_key attribute
    #and have multiple polls saved as bot data.

    print("From Callback state handler", context.bot_data["last_multi_sel"]["chosen"])

    #If you are you are using only state_callbacks you could have stored all results
    # in different keys for context.bot_data by senting the payload_key attribute.
    text="Your replies where:\nPoll1 " \
        +str(poll_widget.answer)+"\nPoll2 "+str(poll_widget2.answer)+\
        "\nPoll3 "+str(context.bot_data["last_multi_sel"]["answer"])

    poll_keyboard =  [[InlineKeyboardButton("Again?", callback_data="newpoll"),]]
    reply_markup = InlineKeyboardMarkup(poll_keyboard)
    context.bot.send_message(update.effective_chat.id, text, reply_markup=reply_markup)  



###################################################################################################

#This was my first test to have the functionality and might be useful if you want to learn what I am doing here:
@deco.run_async
@deco.conversation_command_handler("ideapoll")
def test2(update, context):
    options=["Option 1", "Option 2", "Option 3", "Option 4"]

    dp=context.dispatcher

    keyboard=[[InlineKeyboardButton("_"+"   "+text, callback_data=f"{i}")]
            for i, text in enumerate(options)]

    keyboard.append([InlineKeyboardButton("Confirm", callback_data=f"poll_confirm")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    message=update.message.reply_text('Please choose: ', reply_markup=reply_markup)
    chosen=[]

    def button(update, context):                                                                                             
        query = update.callback_query.data
        print("Query is index: "+str(query))            
        if query=="poll_confirm":
            dp.remove_handler(CallbackQueryHandler(button))
            print(chosen)
            return
        i=int(query)
        if i in chosen:
            keyboard[i][0]=InlineKeyboardButton("_"+options[i], callback_data=f"{i}")        
            chosen.remove(i)
        else:
            keyboard[i][0]=InlineKeyboardButton("V"+options[i], callback_data=f"{i}")
            chosen.append(i)
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.edit_reply_markup(reply_markup=reply_markup)

        
    dp.add_handler(CallbackQueryHandler(button))