from config import *
from wiki import *
from weather import *


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


@bot.message_handler(commands=['wikipedia'])
def ask_wiki(message):
    msg = bot.send_message(message.chat.id, "Введіть пошуковий запит:\n")
    bot.register_next_step_handler(msg, ask_wiki_2)


def ask_wiki_2(message):
    resp = fetch_wikipedia_article(message.text)
    bot.reply_to(message, resp)


@bot.message_handler(commands=['weather'])
def weather_menu(message):
    bot.send_message(message.chat.id, "Оберіть місто для отримання погоди:", reply_markup=weather_keyboard)


@bot.message_handler(commands=['keyboard_test'])
def keyboard_test(message):
    bot.send_message(message.chat.id, text=".", reply_markup=test_keyboard)


def create_user_buttons():
    keyboard = types.InlineKeyboardMarkup()
    users = users_collection.find()
    for user in users:
        button = types.InlineKeyboardButton(
            text=f"{user['name']} {user['surname']}",
            callback_data=f"user_{user['_id']}"
        )
        keyboard.add(button)
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data.startswith('user_'))
def user_info(call):
    user_id = call.data.split('_')[1]
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        info = f"👤 <b>{user['name']} {user['surname']}</b>\n" \
               f"🗓 Вік: {user['age']}\n" \
               f"🚻 Стать: {user['gender']}"
        bot.send_message(call.message.chat.id, info, parse_mode="HTML")
    else:
        bot.send_message(call.message.chat.id, "Користувача не знайдено.")


@bot.message_handler(commands=['users'])
def show_users(message):
    if users_collection.count_documents({}) == 0:
        generate_random_users()

    bot.send_message(message.chat.id, "Список користувачів:", reply_markup=create_user_buttons())


@bot.message_handler(func=lambda message: message.text in ["Kyiv", "Lviv", "Odessa"])
def get_weather(message):
    city = message.text
    weather_info = fetch_weather(city)
    bot.send_message(message.chat.id, f"Погода в {city}:\n{weather_info}")


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


def create_buttons(button_type, count):
    if button_type == 'inline':
        keyboard = types.InlineKeyboardMarkup()
        for i in range(count):
            button = types.InlineKeyboardButton(f"Кнопка {i}", callback_data=f"btn_{i}")
            keyboard.add(button)
    else:  # reply
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(count):
            keyboard.add(types.KeyboardButton(f"Кнопка {i}"))

    return keyboard


@bot.message_handler(commands=['create_buttons'])
def ask_button_details(message):
    msg = bot.send_message(message.chat.id, "Введіть тип кнопок (inline/reply) та кількість через пробіл (наприклад: "
                                            "inline 3):")
    bot.register_next_step_handler(msg, process_button_request)


def process_button_request(message):
    try:
        button_type, count = message.text.split()
        count = int(count)

        if button_type not in ['inline', 'reply']:
            raise ValueError("Неправильний тип кнопок. Використовуйте 'inline' або 'reply'.")

        buttons = create_buttons(button_type, count)
        bot.send_message(message.chat.id, "Ваші кнопки готові:", reply_markup=buttons)

    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Помилка! Введіть коректний тип (inline/reply) та кількість кнопок.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('btn_'))
def button_callback(call):
    bot.send_message(call.message.chat.id, f"Ви натиснули {call.data.replace('btn_', 'Кнопка ')}")


def create_currency_buttons():
    keyboard = types.InlineKeyboardMarkup()
    currencies = ["USD", "EUR", "UAH"]
    for currency in currencies:
        button = types.InlineKeyboardButton(
            text=f"Оплатити у {currency}",
            callback_data=f"pay_{currency}"
        )
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['currency'])
def start_payment(message):
    bot.send_message(
        message.chat.id,
        "Оберіть валюту для оплати:",
        reply_markup=create_currency_buttons()
    )


def generate_invoice(currency):
    amount = 100
    exchange_rate = {
        "USD": 1,
        "EUR": 0.92,
        "UAH": 37
    }
    total = amount * exchange_rate.get(currency, 1)
    return f"{total:.2f} {currency}"


@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def process_payment(call):
    currency = call.data.split('_')[1]
    invoice = generate_invoice(currency)  # Функція генерації рахунку
    bot.send_message(call.message.chat.id, f"Ваш рахунок для оплати в {currency}:\n{invoice}")


@bot.callback_query_handler(func=lambda call: True)
def fallback_handler(call):
    bot.answer_callback_query(call.id, "Невідома команда. Будь ласка, спробуйте ще раз.")


# @bot.message_handler(content_types=['text', 'photo', 'document'])
# def check_on(message):
#     message_text = message.text
#     if message.content_type == "photo" or message.content_type == 'document':
#         if message.caption:
#             message_text = message.caption
#         else:
#             return
#
#     bot.reply_to(message, "gg", reply_markup=remove_reply_keyboard)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
