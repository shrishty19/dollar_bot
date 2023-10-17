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

    def expense_option_selection(message, bot):
    selected_option = message.text
    if selected_option == "Add":
        select_expense_category(message, bot)
    elif selected_option == "Delete":
        delete_expense(message, bot)  # Call the delete_expense function.
    elif selected_option == "Update":
        edit.run(message, bot)  # This calls the edit functionality
    else:
        bot.send_message(message.chat.id, "Invalid option. Please try again.")

def select_expense_category(message, bot):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = helper.getSpendCategories()  # Retrieve the list of categories.
    for c in categories:
        markup.add(c)
    msg = bot.send_message(message.chat.id, "Select Category for expense:", reply_markup=markup)
    bot.register_next_step_handler(msg, expense_category_selected, bot)