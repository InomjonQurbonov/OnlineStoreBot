from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import DB_NAME
from utils.database import Database


db = Database(DB_NAME)


# Function for make inline keyboards from category names
def make_category_list() -> InlineKeyboardMarkup:
    categories = db.get_categories()
    rows = []
    for category in categories:
        rows.append([
            InlineKeyboardButton(
                text=str(category[1]),
                callback_data=str(category[1])
            )
        ])
    kb_categories = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb_categories

def make_products_list() -> InlineKeyboardMarkup:
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