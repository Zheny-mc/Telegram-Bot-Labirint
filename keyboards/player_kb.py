from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_up = InlineKeyboardButton(text='\U0001F53C', callback_data='up')
button_left = InlineKeyboardButton(text='\U000025C0', callback_data='left')
button_down = InlineKeyboardButton(text='\U0001F53D', callback_data='down')
button_right = InlineKeyboardButton(text='\U000025B6', callback_data='right')

kb_player = InlineKeyboardMarkup()
kb_player.add(button_up).row(button_left, button_down, button_right)