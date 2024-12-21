from config import *


@bot.message_handler(commands=['start', 'hello', 'begin'])
def start_message(message):
    # bot.send_message(message.chat.id,
    #                  text="Вітаю!\n", reply_markup=helper)
    bot.send_message(message.chat.id, text="Вітаю!")


@bot.message_handler(commands=['inform'])
def inform_message(message):
    bot.send_message(message.chat.id, text=".", reply_markup=send_photo_keyboard)


@bot.message_handler(commands=['clear_chat'])
def clear_message(message):
    bot.reply_to(message, "Виконую", reply_markup=remove_reply_keyboard)


@bot.message_handler(commands=['keyboard_test'])
def keyboard_test(message):
    bot.send_message(message.chat.id, text=".", reply_markup=test_keyboard)


# @bot.message_handler(commands=['custom'],
#                      func=lambda message: message.from_user.id in ADMINS)
# def ban_card(message):


can_handle = ["send_photo", "keyboard_type_1", "keyboard_type_2", "keyboard_type_3"]


@bot.callback_query_handler(func=lambda call: call.data in can_handle)
def my_dino_buttons(call):
    teleID = call.message.chat.id
    if call.data == "send_photo":
        bot.send_photo(chat_id=call.message.chat.id, photo=open("robot.jpg", 'rb'))
    if call.data == "keyboard_type_1":
        bot.send_message(call.message.chat.id, text="Таблиця кнопок №1", reply_markup=keyboard_1)
    if call.data == "keyboard_type_2":
        bot.send_message(call.message.chat.id, text="Таблиця кнопок №2", reply_markup=keyboard_2)
    if call.data == "keyboard_type_3":
        bot.send_message(call.message.chat.id, text="Таблиця кнопок №3", reply_markup=keyboard_3)


@bot.message_handler(content_types=['text', 'photo', 'document'],
                     func=lambda message: message.from_user.id not in ADMINS)
def check_on(message):
    message_text = message.text
    if message.content_type == "photo" or message.content_type == 'document':
        if message.caption:
            message_text = message.caption
        else:
            return
    bot.reply_to(message, f"Згоден з твердженням \'{message_text}\'", reply_markup=remove_reply_keyboard)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
