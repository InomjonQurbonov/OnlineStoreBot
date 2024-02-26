from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DB_NAME
from states.admin_states import CategoryStates,ProductStates
from utils.database import Database

admin_message_router = Router()
db = Database(DB_NAME)

@admin_message_router.message(CategoryStates.newCategory_state)
async def new_category_handler(message: Message, state: FSMContext):
    res = db.add_category(message.text)
    if res['status']:
        await message.chat.send_message("New category successfully added")
        await state.finish()
    elif res['desc'] == 'exists':
        await message.reply("This category already exists.\n"
                            "Please, send another name or click /cancel")
    else:
        await message.reply(res['desc'])

@admin_message_router.message(CategoryStates.delCategory_state)
async def del_category_handler(message: Message, state: FSMContext):
    res = db.delete_category(message.text)
    if res:
        await message.chat.send_message(f"Category {message.text} deleted successfully")
        await state.finish()
    else:
        await message.chat.send_message(f"Category {message.text} not found or can't be deleted")

@admin_message_router.message(ProductStates.newProduct_state)
async def new_product_handler(message: Message, state: FSMContext):
    res = db.add_product(message.text,message.photo)
    if res['status']:
        await message.chat.send_message("New product successfully added")
        await state.finish()
    elif res['desc'] == 'exists':
        await message.reply("This product already exists.\n"
                            "Please, send another name or click /cancel")
    else:
        await message.reply(res['desc'])

@admin_message_router.message(ProductStates.delProduct_state)
async def del_product_handler(message: Message, state: FSMContext):
    res = db.delete_products(message.text)
    if res:
        await message.chat.send_message(f"Category {message.text} deleted successfully")
        await state.finish()
    else:
        await message.chat.send_message(f"Category {message.text} not found or can't be deleted")