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
        edit.run(message, sbot)  # This calls the edit functionality
    else:
        bot.send_message(message.chat.id, "Invalid option. Please try again.")

def select_expense_category(message, bot):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = helper.getSpendCategories()  # Retrieve the list of categories.
    for c in categories:
        markup.add(c)
    msg = bot.send_message(message.chat.id, "Select Category for expense:", reply_markup=markup)
    bot.register_next_step_handler(msg, expense_category_selected, bot)

def expense_category_selected(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, "Invalid", reply_markup=telebot.types.ReplyKeyboardRemove())
            raise Exception(f'Sorry, I don\'t recognize this category "{selected_category}"!')

        markup = telebot.types.ReplyKeyboardRemove()
        msg = bot.send_message(chat_id, f"How much did you spend on {selected_category}?", reply_markup=markup)
        bot.register_next_step_handler(msg, record_expense, selected_category, bot)
    except Exception as e:
        bot.reply_to(message, "Oh no! " + str(e))

        def record_expense(message, category, bot):
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate

        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today().strftime(helper.getDateFormat() + " " + helper.getTimeFormat())
        record_to_be_added = "{},{},{}".format(str(date_of_entry), category, str(amount_value))

        helper.write_json(add_user_record(chat_id, record_to_be_added))

        bot.send_message(chat_id, f"You have spent ${amount_value} for {category} on {date_of_entry}")
        helper.display_remaining_budget(message, bot, category)
    except Exception as e:
        bot.reply_to(message, "Oh no. " + str(e))

        def delete_expense(message, bot):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    expenses = helper.getUserHistory(message.chat.id)  # Get user's expense history.
    for expense in expenses:
        markup.add(expense)

    msg = bot.send_message(message.chat.id, "Select the expense to delete:", reply_markup=markup)
    bot.register_next_step_handler(msg, confirm_delete_expense, bot)