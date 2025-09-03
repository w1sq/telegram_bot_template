from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Меню", callback_data="user_prompt")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
