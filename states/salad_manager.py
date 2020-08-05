from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
                          Filters)

from telegram.utils.helpers import mention_html
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from random import choice
from settings import CHATID
from time import sleep

#cbs = "approve_salads"
#@deco.register_state_callback(states.SECOND, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True, pass_update_queue=True)
@deco.run_async
def salad_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    print("SALAD POLL DATA" + str(data))
    user_data = context.user_data
    user_id = user_data['user_id']
    tortia_selection = context.user_data['TortiaSelection']
    randomCartId = context.user_data['CartId']
    product_keyboard = []
    
    bot_data = context.bot_data

    #print("BOT DATA ********** " + str(bot_data))

    #first_poll_answers = context.user_data['FirstSaladPollAnswers']
    #print("FIRST POLL ANSWERS: ??? " + str(first_poll_answers))
    answer = update.poll_answer
    print("ANSWER:" + str(answer))
    poll_id = first_poll_id
    try:
        questions = context.bot_data[poll_id]["questions"]
        answers = context.bot_data[poll_id]["answers"]
        print(questions)
        print(answers)
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return

    user_mention = mention_html(update.effective_user.id, update.effective_user.full_name)
    context.bot.send_message(context.bot_data[poll_id]["chat_id"],
                             "{} feels {}!".format(user_mention, answers),
                             parse_mode=ParseMode.HTML)
        # Close poll after three participants voted
    if context.bot_data[poll_id]["answers"] == 0:
        context.bot.stop_poll(context.bot_data[poll_id]["chat_id"],
                              context.bot_data[poll_id]["message_id"])

    
    salads_for_tort_jab = ["חמוצים", "סלט בצל לא חריף", "סלט ירקות (עבניה, מלפפון)", "סלט חסה", "סלט בצל חריף"]
    extra_onside = ["צ\'יפס", "טבעות בצל", "כרובית", "פוטטוס"]
    
    reply_text = emojize("\n \U0000200F בחירתכם {} התקבלה.")
    approve_salad = emojize("\U0000200F \U000021AA אישור בחירה")
    back_button = emojize("\U0000200F \U000021AA חזרה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")
    
    product_keyboard +=  [[InlineKeyboardButton(approve_salad, callback_data="cb_extra_manager")],[InlineKeyboardButton(back_button, callback_data="cb_back_tortias"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_tortia_salad = InlineKeyboardMarkup(product_keyboard)

    message = context.bot.send_poll(update.effective_user.id, "לבחירתכם תוספת אחת מהמנות הבאות: \n",
                                type="regular", 
                                options=extra_onside,
                                is_anonymous=False, 
                                allows_multiple_answers=True,
                                reply_markup=reply_markup_tortia_salad)

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {message.poll.id: {"questions": extra_onside, "message_id": message.message_id,
                                 "chat_id": update.effective_chat.id, "answers": 0}}

    print("SECOND PAYLOAD MSG ID: >>>> " + str(message.message_id))
    print("SECOND POLL ID: >>>> " + str(message.poll.id))
    context.user_data['ExtraPollMessageId'] = message.message_id
    context.user_data['ExtraPollId'] = message.poll.id
    context.bot_data.update(payload)

    return states.FIRST
