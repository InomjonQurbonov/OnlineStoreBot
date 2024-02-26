from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import DB_NAME
from utils.database import Database


db = Database(DB_NAME)


# Function for make inline keyboards from category names
def get_category_list() -> InlineKeyboardMarkup:
    categories = db.get_categories()
    rows = []
    for category in categories:
        rows.append([
            InlineKeyboardButton(
                text=category[1],
                callback_data=str(category[0])
            )
        ])
    kb_categories = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb_categories


# Function for make inline keyboards from product names
def get_products(category) -> InlineKeyboardMarkup:
    products = db.get_products()
    rows = []
    for product in products:
        rows.append([
            InlineKeyboardButton(
                text=str(product[1]),
                callback_data=str(product[1])
            )
        ])
    kb_products = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb_products

def get_ads_list() -> InlineKeyboardMarkup:
    adds = db.get_adds()
    rows = []
    for add in adds:
        rows.append([
            InlineKeyboardButton(
                text=str(add[1]),
                callback_data=str(add[1])
            )
        ])
    kb_adds = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb_adds

left_right_k = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️",callback_data="left"),
     InlineKeyboardButton(text="➡️",callback_data="right")]
])
def search_button(num_buttons):
    inline_keyboard = [
        InlineKeyboardButton(text=f"{i+1}️⃣", callback_data=f"{i+1}") for i in range(num_buttons)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

