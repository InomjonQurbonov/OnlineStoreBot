from aiogram.fsm.state import State, StatesGroup


class ClientAdsStates(StatesGroup):
    selectAd = State()
    showAllAds = State()
    searchAds = State()
    selectAdCategory = State()
    selectAdProduct = State()

    insertTitle = State()
    insertText = State()
    insertPrice = State()
    insertImages = State()
    insertPhone = State()

    updTitle = State()
    updText = State()
    updPrice = State()
    updImages = State()
    updPhone = State()

    delAd = State()
    del_Ad_confirm = State()
    del_Ad_list = State()