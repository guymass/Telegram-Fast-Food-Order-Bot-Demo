from telegram.ext import PollAnswerHandler
import logging
from warnings import warn
from lib import deco
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
poll_data=[]

def clear_poll_data():
    poll_data=[]    

def poll_callback(update, context):
    answer = update.poll_answer
    poll_id = answer.poll_id        
    poll_callback=context.bot_data[poll_id]["poll_callback"]
    data=context.bot_data[poll_id]
    data.update({"answers": answer['option_ids']})
    poll_data.append(context.bot_data[poll_id])
    logging.info("handling poll: "+str(poll_id)+ "----  With callback: "+str(poll_callback))
    if poll_callback in deco.poll_handlers:
        #TODO support multiple states (same keys) instead of just the last added
        i=-1
        deco.poll_handlers[poll_callback][i](update, context, answer=answer['option_ids'], chat_id=context.bot_data[poll_id]["chat_id"])
    else:
        warn("Poll callback not implemented!")

def generate_keyboard(button_name_list, callback_list, n_columns):
    """
    Facilitator function for generating a simple and symmetrical keyboard.
    Parameters
    ----------
    button_name_list : List[str]
        List of strings that define the button's texts
    callback_list : List[str]
        List of strings that define the callbacks. Must have the same size as button_name_list
    n_columns : int
        Number of columns
    Returns : List[List[InlineKeyboardButton]]
    """
    assert len(button_name_list)==len(callback_list), "button_name_list and callback_list must be same size"
    n_rows=int(len(button_name_list)/n_columns)
    keyboard=[[InlineKeyboardButton(button_name_list[i*n_columns+j], callback_data=callback_list[i*n_columns+j]) 
            for j in range(0,n_columns)] for i in range(n_rows)]
    if add:=len(button_name_list)%n_columns > 0:
        i=len(button_name_list)-add
        keyboard.append([InlineKeyboardButton(button_name_list[j], callback_data=callback_list[j]) 
                for j in range(i,len(button_name_list))])
    return keyboard


def emulate_callback_query(update, context, callback_data):
    """
    This function emulates a callbackQuery event
    """
   
    ## This is real would be real update emulation on the telegram python lib level
    #from telegram import Update, CallbackQuery
    #import random
    #import string
    
    #letters = string.ascii_letters
    #user=update.effective_user
    #chat=update.effective_chat
    #callback_query=CallbackQuery("emulated_query_"+''.join(random.choice(letters) for i in range(4)), user, chat, data=callback_data)
    #new_update=Update(update.update_id+1, callback_query=callback_query)    
    #context.update_queue.put(new_update)

    # This is a cheap trick
    if callback_data in deco.entry_states:  
        deco.entry_states[callback_data][-1].callback(update, context)

class buttons_menu():
    def __init__(self, buttons_dict, question="Choose: ", n_columns=1):
        """
        buttons_dict : {callback : button_text}
        question : str
        n_columns : int 
            Number of columns in menu
        """
        self.buttons_dict=buttons_dict
        self.n_columns=n_columns
        self.options=[self.buttons_dict[k] for k in self.buttons_dict]
        self.callbacks=[k for k in self.buttons_dict]
        self.question=question

    def create_kb(self):
        """
        Generates the keyboard for the widget
        """
        n_columns=self.n_columns
        button_name_list=self.options
        self.handler=CallbackQueryHandler(lambda u,c: deco.send_typing_action(self.button_handler(u, c)))
        self.keyboard=generate_keyboard(self.options, self.callbacks, n_columns)
        self.dp.add_handler(self.handler)
    
    def finalize(self):
        self.dp.remove_handler(self.handler)
        self.message.delete()

    def send(self, update, context):
        self.dp=context.dispatcher
        self.create_kb()
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)
        self.message=context.bot.send_message(update.effective_chat.id, self.question, reply_markup=self.reply_markup)  

    def button_handler(self, update, context):                                                                                             
        query = update.callback_query.data
        emulate_callback_query(update, context, query)
        self.finalize()

class multi_selection_widget():
    """
    Parameters
    ----------
    options : List[str]
        A list of the names for each of the checkable buttons (default is [])
    question : str
        Question to ask before the poll
    add_confirm_button : bool
        If set to False the pool wont have the confirm button. See add extra buttons. The callback and callback_data will still work. (default True)
    spacing : int 
        Number of spaces between check symbol and text. (default 5)
    callback : function
        Function to be called when the confirm button is pressed (optional)
    callback_data : str
        Callback data to be passed to the update queue. This will emulate a callback on the telegram api (optional)
    extra_buttons : List[telegram.ext.InlineKeyboardButton]
        Extra buttons to append to the end of the widget. This is useful to add extra functionality. You will have to set the callback handlers for them manually. (optional)
    confirm_button_text : str
        Text for the confirmation button (default is "confirm")
    single_option : boolean
        If true  it will be possible to select  only one option (default is False)
    n_columns : int 
        Number of columns of the widget (default is 1)
    checked_symbol : str
        Character or string to prepend on the button's text when state is checked
    unchecked_symbol : str 
        Character or string to prepend on the button's text when state is unchecked
    autoremove : bool
        If False the widget won't be deleted after confirm is pressed by the user. (default is True)
    payload_key : str
        Name of the payload to add in bot_data that can be useful in a callbackQuery handler. This is only set if callback_data is set. (default "last_multi_sel")
    Attributes
    --------
    chosen : List[int]
        List of indexes of options that are currently checked
    answer : List[str]
        List of the button text names that were chosen
    update : telegramUpdater
    context : telegram.ext.CallbackContext
    reply_markup
    dp : telegram.ext.Dispatcher
    keyboard : List[List[InlineKeyboardButton]]
    """
    def __init__(self, options=[], question="אמא בחרו:  " ,
    add_confirm_button=True, spacing=5, callback=None, callback_data=None, 
    extra_buttons=[], cancel_buttons=[], confirm_button_text="אישור", single_option=False, n_columns=1, 
    checked_symbol="✓", unchecked_symbol="✗", autoremove=True,payload_key="last_multi_sel",
    chosen=[], alert_message_text="אנא בחרו לפחות תוספת אחת מהרשימה."):
        """
        Parameters
        ----------
        options : List[str]
        question : str
        add_confirm_button : bool
        spacing : int
        callback : function
        callback_data : str
        extra_buttons : List[telegram.ext.InlineKeyboardButton]
        confirm_button_text : str
        single_option : boolean
        n_columns : int 
        checked_symbol : str
        unchecked_symbol : str 
        autoremove : bool
        payload_key : str
        """
        self.options=options
        self.add_confirm_button=add_confirm_button
        self.single_option=single_option
        self.n_columns=n_columns
        self.spacing=spacing
        self.confirm=self.confirm_button_text=confirm_button_text
        self.extra_buttons=extra_buttons
        self.checked=self.checked_symbol=checked_symbol
        self.unchecked=self.unchecked_symbol=unchecked_symbol
        self.autoremove=autoremove
        self.callback=callback
        self.callback_data=callback_data
        self.question=question
        self.payload_key=payload_key
        self.chosen=chosen
        self.alert_message_text=alert_message_text
        self.cancel_buttons=cancel_buttons 
        self.cancel_buttons_callbacks=[]

        for btn in cancel_buttons:
            self.cancel_buttons_callbacks.append(btn.callback_data)

    def create_kb(self):
        """
        Generates the keyboard for the widget
        """
        n_columns=self.n_columns
        button_name_list=self.options
        self.keyboard=generate_keyboard([f"{self.checked if i in self.chosen else self.unchecked}{' '*self.spacing}{t}" for i,t in enumerate(button_name_list)],list(range(len(button_name_list))), n_columns)
        self.handler=CallbackQueryHandler(lambda u, c: self.button_handler(u, c))
        self.dp.add_handler(self.handler)
        if self.add_confirm_button:
            self.keyboard.append([InlineKeyboardButton(self.confirm_button_text, callback_data=f"multi_sel_confirmation")])
        self.keyboard.append(self.extra_buttons)
        self.keyboard.append([InlineKeyboardButton(btn.text, callback_data=f"multi_sel_cancel_button_{i}") for i,btn in enumerate(self.cancel_buttons)])
    
    def send(self, update, context, restore=False):
        """
        Generates the keyboard, sets up the button handlers and sends the message to the current update chat.
        Parameters
        ----------
        update : TelegramUpdater
        context : Telegram.ext.CallbackContext
        restore : bool
            Restores the last state from user_data by using the payload_key.
        """        
        #TODO check if user_data is compatible before attempting restore     
        self.dp=context.dispatcher
        self.context=context
        self.update=update
        print("payload: ", self.payload_key)
        print("keys: ", [k for k  in self.context.user_data])
        if restore:            
            try:
                chosen=[] if self.payload_key in self.context.user_data and len(self.context.user_data[self.payload_key])==0 else self.context.user_data[self.payload_key]["chosen"]
                if (self.single_option and len(chosen)>1) or len(chosen)>len(self.options):
                    chosen=[]
                self.chosen=chosen
            except KeyError:
                pass
            print("Restoring chosen indexes: ", self.chosen)
        else:
            self.chosen=[]
        self.create_kb()
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)
        self.message=context.bot.send_message(update.effective_chat.id, self.question, reply_markup=self.reply_markup)    

    def find_indexes(self,i):
        """
        Finds the indexes in the keyboard for a given index of the options list.
        Parameters
        ------------
        i : int
            The index of the button. Notice that this index corresponds to an index  in the options attribute and not on the keyboard itself, ignoring the number of rows.
            
        Returns : int
            j,k indexes of corresponding self.keyboard[j][k]
        """
        indexes=[]
        c=0
        for j,row in enumerate(self.keyboard):
            for k,btn in enumerate(row):
                if c==i:
                    indexes=[j, k]
                    break
                c+=1
            if indexes: break  
        return j,k

    def toggle_check(self,i):
        """
        Toggles the check state of a button, updating the chosen list attribute.
        Parameters
        ---------
        i : int
            The index of the button. Notice that this index corresponds to an index  in the options attribute and not on the keyboard itself, ignoring the number of rows.
        """
        j,k=self.find_indexes(i)
        #print("Chosen is: ", self.chosen)
        if i in self.chosen:
            self.keyboard[j][k]=InlineKeyboardButton(f"{self.unchecked}{' '*self.spacing}"+self.options[i], callback_data=f"{i}")        
            self.chosen.remove(i)
        else:
            if len(self.chosen) == 1 and self.single_option:
                self.toggle_check(self.chosen[0])
            print(self.keyboard[j][k])
            print(self.options)
            print(self.options[i])
            self.keyboard[j][k]=InlineKeyboardButton(f"{self.checked}{' '*self.spacing}"+self.options[i], callback_data=f"{i}")
            self.chosen.append(i)        

    def _delete_alert_msg(self):
        try:
            if not self.alert_message is None:
                self.alert_message.delete()
        except:
            pass    


    def _set_payload(self):
        payload = {
            self.payload_key: {
                "questions": self.options, 
                "message_id": self.message.message_id, 
                "chat_id": self.update.effective_chat.id, 
                "answer": self.answer, 
                "chosen": self.chosen
                }
            }
        self.context.user_data.update(payload)

    def finalize(self, cancel=False):
        """
        Forces finishing the widget even if any option was checked
        """
        self.dp.remove_handler(self.handler)
        self.answer=[self.options[i] for i in self.chosen]       
        self._delete_alert_msg()
        if self.autoremove:
            self.message.delete()
        if not self.callback is None:
            self._set_payload()
            if not cancel:
                self.callback(self, self.update, self.context)
        if not self.callback_data is None:
            self._set_payload()
            if not cancel:
                emulate_callback_query(self.update, self.context, self.callback_data)
        return self.chosen

    def end(self):
        """
        Finalizes the widget at least one option was marked
        """
        if len(self.chosen):
            self.finalize()
        else:
            self._delete_alert_msg()
            self.alert_message=self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.alert_message_text)

    def button_handler(self, update, context):                                                                                             
        query = update.callback_query.data
        if query=="multi_sel_confirmation":
            self.end()
        elif query.startswith("multi_sel_cancel_button"):
            self.finalize(True)
            index=int(query[-1])
            query=self.cancel_buttons_callbacks[index]
            deco.entry_states[query][-1].callback(update, context)
        elif query in deco.entry_states:  #Give preference for already registered states            
            deco.entry_states[query][-1].callback(update, context)
        else:
            try:
                i=int(query)
                self.toggle_check(i)
                self.reply_markup = InlineKeyboardMarkup(self.keyboard)
                self.message.edit_reply_markup(reply_markup=self.reply_markup)
            except ValueError:
                print("Unregistered callback: ", query)

