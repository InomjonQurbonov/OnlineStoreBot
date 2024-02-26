from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from config import DB_NAME, admins
from keyboards.admin_inline_keyboards import make_category_list,make_products_list
from states.admin_states import CategoryStates,ProductStates
from utils.database import Database
from utils.my_commands import commands_admin, commands_user

commands_router = Router()
db = Database(DB_NAME)


@commands_router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=commands_admin)
        await message.answer("Welcome admin, please choose command from commands list")
    else:
        await message.bot.set_my_commands(commands=commands_user)
        await message.answer("Let's start registration")


@commands_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("All actions canceled, you may continue sending commands")


# With this handler admin can add new category
@commands_router.message(Command('new_category'))
async def new_category_handler(message: Message, state: FSMContext):
    await state.set_state(CategoryStates.newCategory_state)
    await message.answer("Please, send new category name ...")


# Functions for editing category name
@commands_router.message(Command('edit_category'))
async def edit_category_handler(message: Message, state: FSMContext):
    await state.set_state(CategoryStates.updCategory_state_list)
    await message.answer(
        text="Choose category name which you want to change...",
        reply_markup=make_category_list()
    )
# Function to delete category
@commands_router.message(Command('del_category'))
async def delete_category_handler(message: Message, state: FSMContext):
    await state.set_state(CategoryStates.delCategory_state_list)
    await message.answer(
        text="Choose category name which you want to delete...",
        reply_markup=make_category_list()
    )
# Fuction  add product to category
@commands_router.message(Command('new_product'))
async def add_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductStates.newProduct_state)
    await message.answer("Please, send new product name,product image and product category:")

@commands_router.message(Command('edit_product'))
async def edit_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductStates.editProduct_state)
    await message.answer("Please, send the product id and the new product name, product image, and product category you want to update:")

@commands_router.message(Command('categories'))
async def list_categories_handler(message: Message,state: FSMContext):
    await state.set_state(CategoryStates.listCategory_state)
    await message.answer(
        text="All category list...",
        reply_markup=make_category_list()
    )

@commands_router.message(Command('products'))
async def list_products_handler(message: Message,state: FSMContext):
    await state.set_state(ProductStates.listProduct_state)
    await message.answer(
        text="All products list...",
        reply_markup=make_products_list()
    )

@commands_router.message(Command('del_product'))
async def delete_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductStates.delProduct_state_list)
    await message.answer(
        text="Choose product name which you want to delete...",
        reply_markup=make_products_list()
    )


@commands_router.callback_query(CategoryStates.updCategory_state_list)
async def callback_category_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cat_name=callback.data)
    await state.set_state(CategoryStates.updCategory_state_new)
    await callback.message.answer(f"Please, send new name for category '{callback.data}'")
    await callback.message.delete()

@commands_router.message(CategoryStates.updCategory_state_new)
async def set_new_category_name(message: Message, state: FSMContext):
    new_cat = message.text
    st_data = await state.get_data()
    old_cat = st_data.get('cat_name')
    res = db.upd_category(message.text, old_cat)
    if res['status']:
        await message.answer("Category name successfully changed")
        await state.clear()
    elif res['desc'] == 'exists':
        await message.reply("This category already exists.\n"
                            "Please, send other name or click /cancel")
    else:
        await message.reply(res['desc'])

@commands_router.callback_query(CategoryStates.delCategory_state_list)
async def callback_category_delete(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cat_name=callback.data)
    await state.set_state(CategoryStates.delCategory_state_confirm)
    await callback.message.answer(f"Are you sure you want to delete the category '{callback.data}'?")

@commands_router.message(CategoryStates.delCategory_state_confirm)
async def confirm_category_delete(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        st_data = await state.get_data()
        cat_name = st_data.get('cat_name')
        res = db.delete_category(cat_name)
        if res['status']:
            await message.answer("Category successfully deleted")
            await state.clear()
        else:
            await message.reply(res['desc'])
    else:
        await message.reply("Category deletion cancelled")
        await state.clear()


@commands_router.message(ProductStates.newProduct_state)
async def set_new_product(message: Message, state: FSMContext):
    product_data = []
    if message.photo:
        photo_id = message.photo[-1].file_id
        caption = message.caption.split(',')
        for text in caption:
            product_data.append(text)
        product_data.insert(1, photo_id)
    else:
        product_data = message.text.split(',')

    if len(product_data) != 3:
        await message.reply("Please, send product name, product image, and product category")
    else:
        product_name = product_data[0]
        product_image = product_data[1]
        product_category = product_data[2]
        res = db.add_product(product_name, product_image, product_category)
        if res['status']:
            await message.answer("Product successfully added")
            await state.clear()
        else:
            await message.reply(res['desc'])

@commands_router.message(ProductStates.editProduct_state)
async def edit_product(message: Message, state: FSMContext):
    product_data = []
    if message.photo:
        photo_id = message.photo[-1].file_id
        caption = message.caption.split(',')
        for text in caption:
            product_data.append(text)
        product_data.insert(2, photo_id)
    else:
        product_data = message.text.split(',')

    print(len(product_data))
    print(product_data)

    if len(product_data) != 4:
        await message.reply("Please, send product id, product name, product image, and product category")
    else:
        product_id = product_data[0]
        product_name = product_data[1]
        product_image = product_data[2]
        product_category = product_data[3]
        res = db.edit_product(product_id, product_name, product_image, product_category)
        if res['status']:
            await message.answer("Product successfully updated")
            await state.clear()
        else:
            await message.reply(res['desc'])

@commands_router.callback_query(ProductStates.delProduct_state_list)
async def callback_product_delete(callback: CallbackQuery, state: FSMContext):
    await state.update_data(product_name=callback.data)
    await state.set_state(ProductStates.delProduct_state_confirm)
    await callback.message.answer(f"Are you sure you want to delete the product '{callback.data}'?")

@commands_router.message(ProductStates.delProduct_state_confirm)
async def confirm_product_delete(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        st_data = await state.get_data()
        product_name = st_data.get('product_name')
        res = db.delete_products(product_name)
        if res['status']:
            await message.answer("Product successfully deleted")
            await state.clear()
        else:
            await message.reply(res['desc'])
    else:
        await message.reply("Product deletion cancelled")
        await state.clear()

