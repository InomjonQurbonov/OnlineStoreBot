from aiogram.fsm.state import State, StatesGroup


class CategoryStates(StatesGroup):
    newCategory_state = State()
    listCategory_state = State()

    updCategory_state_list = State()
    updCategory_state_new = State()

    delCategory_state = State()
    delCategory_state_confirm = State()
    delCategory_state_list = State()

class ProductStates(StatesGroup):
    newProduct_state = State()
    listProduct_state = State()

    editProduct_state = State()

    delProduct_state = State()
    delProduct_state_confirm = State()
    delProduct_state_list = State()