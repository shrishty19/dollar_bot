import telebot
import helper
import edit
from datetime import datetime

def process_expense_command(message, bot):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = ["Add", "Delete", "Update"]
    for opt in options:
        markup.add(opt)
    msg = bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    bot.register_next_step_handler(msg, expense_option_selection, bot)