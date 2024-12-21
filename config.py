from connection import *

NAZAR_ID = 368484669
ADMINS = [NAZAR_ID]

########################### INLINE KEYBOARDS ##########################################################################

send_photo_keyboard = types.InlineKeyboardMarkup()
send_photo_keyboard.add(types.InlineKeyboardButton(text='Відправ мені фото', callback_data='send_photo'))

#######################################################################################################################

########################### REPLY KEYBOARDS ##########################################################################

test_keyboard = types.InlineKeyboardMarkup()
test_keyboard.add(types.InlineKeyboardButton(text='Таблиця кнопок №1', callback_data='keyboard_type_1'))
test_keyboard.add(types.InlineKeyboardButton(text='Таблиця кнопок №2', callback_data='keyboard_type_2'))
test_keyboard.add(types.InlineKeyboardButton(text='Таблиця кнопок №3', callback_data='keyboard_type_3'))

keyboard_1 = types.ReplyKeyboardMarkup()
keyboard_1.add(types.KeyboardButton(text='1'), types.KeyboardButton(text='2'), types.KeyboardButton(text='3'))

keyboard_2 = types.ReplyKeyboardMarkup()
keyboard_2.add(types.KeyboardButton(text='1'))
keyboard_2.add(types.KeyboardButton(text='2'), types.KeyboardButton(text='3'), types.KeyboardButton(text='4'))

keyboard_3 = types.ReplyKeyboardMarkup()
keyboard_3.add(types.KeyboardButton(text='1'), types.KeyboardButton(text='2'))
keyboard_3.add(types.KeyboardButton(text='3'), types.KeyboardButton(text='4'), types.KeyboardButton(text='5'))

remove_reply_keyboard = telebot.types.ReplyKeyboardRemove()

#######################################################################################################################
