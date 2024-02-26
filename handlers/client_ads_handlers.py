from time import time
from aiogram import Router,F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from config import DB_NAME
from keyboards.client_inline_keyboard import get_category_list, get_ads_list,left_right_k,search_button
from states.client_states import ClientAdsStates
from utils.database import Database
from unidecode import unidecode

ads_router = Router()
db = Database(DB_NAME)

@ads_router.message(Command('ads'))
async def all_ads_handler(message: Message, state: FSMContext):
    all_ads = db.get_my_ads(message.from_user.id)
    all_ads_list = list(all_ads)
    all_ads_count = len(all_ads_list)
    if all_ads_count == 0:
        await message.answer("You've no any ads")
    elif all_ads_count == 1:
        await message.answer_photo(
            photo=all_ads_list[0][4],
            caption=f"<b>{all_ads_list[0][1]}</b>\n\n{all_ads_list[0][2]}\n\nPrice: ${all_ads_list[0][3]}",
            parse_mode=ParseMode.HTML
        )
    else:
        await state.set_state(ClientAdsStates.showAllAds)
        await state.update_data(all_ads=all_ads_list)
        await state.update_data(index=0)
        await message.answer_photo(
            photo=all_ads_list[0][4],
            caption=f"<b>{all_ads_list[0][1]}</b>\n\n{all_ads_list[0][2]}\n\nPrice: ${all_ads_list[0][3]}\n\n Ad 1 from {all_ads_count}.",
            parse_mode=ParseMode.HTML,
            reply_markup=left_right_k
        )

@ads_router.callback_query(ClientAdsStates.showAllAds)
async def show_all_ads_handler(callback: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    index = all_data.get('index', None)
    all_ads = all_data.get('all_ads', None)

    if callback.data == 'right':
        if index == len(all_ads)-1:
            index = 0
        else:
            index = index + 1
        await state.update_data(index=index)

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=all_ads[index][4],
                caption=f"<b>{all_ads[index][1]}</b>\n\n{all_ads[index][2]}\n\nPrice: ${all_ads[index][3]}\n\n Ad {index+1} from {len(all_ads)}.",
                parse_mode=ParseMode.HTML
            ),
            reply_markup=left_right_k
        )
    else:
        if index == 0:
            index = len(all_ads) - 1
        else:
            index = index - 1

        await state.update_data(index=index)

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=all_ads[index][4],
                caption=f"<b>{all_ads[index][1]}</b>\n\n{all_ads[index][2]}\n\nPrice: ${all_ads[index][3]}\n\n Ad {index+1} from {len(all_ads)}.",
                parse_mode=ParseMode.HTML
            ),
            reply_markup=left_right_k
        )

@ads_router.message(Command('new_ad'))
async def new_ad_handler(message: Message, state: FSMContext):
    await state.set_state(ClientAdsStates.selectAdCategory)
    await message.answer("Please, choose a category for your ad: ", reply_markup=get_category_list())

@ads_router.callback_query(ClientAdsStates.selectAdCategory)
async def select_ad_product(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ClientAdsStates.insertTitle)
    await state.update_data(ad_product=callback.data)
    await callback.message.answer(f"Please, send title for your ad!\n\n"
                                  f"For example:\n"
                                  f"\t- iPhone 15 Pro Max 8/256 is on sale\n"
                                  f"\t- Macbook Pro 13\" M1 8/256 is on sale")


@ads_router.message(ClientAdsStates.insertTitle)
async def ad_title_handler(message: Message, state: FSMContext):
    await state.update_data(ad_title=message.text)
    await state.set_state(ClientAdsStates.insertText)
    await message.answer("OK, please, send text (full description) for your ad.")


@ads_router.message(ClientAdsStates.insertText)
async def ad_text_handler(message: Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await state.set_state(ClientAdsStates.insertPrice)
    await message.answer("OK, please, send price for your ad (only digits).")


@ads_router.message(ClientAdsStates.insertPrice)
async def ad_price_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(ad_price=int(message.text))
        await state.set_state(ClientAdsStates.insertImages)
        await message.answer("OK, please, send image(s) for your ad.")
    else:
        await message.answer("Please, send only numbers...")


@ads_router.message(ClientAdsStates.insertImages)
async def ad_photo_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(ad_photo=message.photo[-1].file_id)
        await state.set_state(ClientAdsStates.insertPhone)
        await message.answer("OK, please, send phone number for contact with you.")
    else:
        await message.answer("Please, send image(s)...")


@ads_router.message(ClientAdsStates.insertPhone)
async def ad_phone_handler(message: Message, state: FSMContext):
    await state.update_data(ad_phone=message.text)
    all_data = await state.get_data()

    try:
        x = db.insert_ad(
            title=all_data.get('ad_title'),
            text=all_data.get('ad_text'),
            price=all_data.get('ad_price'),
            image=all_data.get('ad_photo'),
            phone=all_data.get('ad_phone'),
            u_id=message.from_user.id,
            prod_id=all_data.get('ad_product'),
            date=time()
        )

        if x:
            await state.clear()
            await message.answer("Your ad has been successfully added!")
        else:
            await message.answer("Something went wrong, please try again later...")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

# edit ads
@ads_router.message(Command('edit_ad'))
async def edit_ads_handler(message: Message, state: FSMContext):
    await state.set_state(ClientAdsStates.selectAd)
    await message.answer("Please, choose an ad for editing:", reply_markup=get_ads_list())



@ads_router.callback_query(ClientAdsStates.selectAd)
async def upd_ad_product(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ClientAdsStates.updTitle)
    id = callback.data
    await state.update_data(ads_title=id)
    await state.update_data(ad_product=callback.data)
    await callback.message.answer("Please, send title for your edited ad!")


@ads_router.message(ClientAdsStates.updTitle)
async def upd_title_handler(message: Message, state: FSMContext):
    await state.update_data(ad_title=message.text)
    await state.set_state(ClientAdsStates.updText)
    await message.answer("OK, please, send text (full description) for your ad.")

@ads_router.message(ClientAdsStates.updText)
async def upd_text_handler(message: Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await state.set_state(ClientAdsStates.updPrice)
    await message.answer("OK, please, send price for your ad (only digits).")


@ads_router.message(ClientAdsStates.updPrice)
async def upd_price_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(ad_price=int(message.text))
        await state.set_state(ClientAdsStates.updImages)
        await message.answer("OK, please, send image(s) for your ad.")
    else:
        await message.answer("Please, send only numbers...")


@ads_router.message(ClientAdsStates.updImages)
async def upd_photo_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(ad_photo=message.photo[-1].file_id)
    else:
        await message.answer("Please, send image(s)...")
    all_data = await state.get_data()
    try:
        x = db.edit_ad(
            upd_title=all_data.get('ad_title'),
            upd_text=all_data.get('ad_text'),
            upd_price=all_data.get('ad_price'),
            upd_image=all_data.get('ad_photo'),
            upd_date=time(),
            ad_title=all_data.get('ads_title')
        )

        if x:
            await state.clear()
            await message.answer("Your ad has been successfully edited!")
        else:
            await message.answer("Something went wrong, please try again later...")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

@ads_router.message(Command('del_ad'))
async def del_ad_handler(message: Message, state: FSMContext):
    await state.set_state(ClientAdsStates.del_Ad_list)
    await message.answer("Please, choose an ad for delete:", reply_markup=get_ads_list())

@ads_router.callback_query(ClientAdsStates.del_Ad_list)
async def callback_Ad_delete(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ad_title=callback.data)
    await state.set_state(ClientAdsStates.del_Ad_confirm)
    await callback.message.answer(f"Are you sure you want to delete the Ad '{callback.data}'?")


@ads_router.message(ClientAdsStates.del_Ad_confirm)
async def confirm_Ad_delete(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        st_data = await state.get_data()
        ad_title = st_data.get('ad_title')
        res = db.delete_ad(ad_title)
        if res['status']:
            await message.answer("Ad successfully deleted")
            await state.clear()
        else:
            await message.reply(res['desc'])
    else:
        await message.reply("Ad deletion cancelled")
        await state.clear()

def normalize_keyword(keyword):
    return (unidecode(keyword))

@ads_router.message()
async def search_ads(message: Message, state: FSMContext):
    ad_title = normalize_keyword(message.text)
    ads = db.search_ads(ad_title)
    adslist = db.ads_list(ad_title=ad_title)

    if not adslist:
        await message.answer(f"No ads found for the keyword '{ad_title}'.")
    else:
        # Save the ads to state
        await state.update_data(ads=adslist)

        # Show the first ad
        ad = adslist[0]
        reply_markup = search_button(min(len(adslist), 5))
        await message.answer(
            text=f"Ad 1 of {len(adslist)}\n\n<b>1 - {ad[1]}</b>\n\n Price: ${ad[3]}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

@ads_router.callback_query(lambda c: c.data.isdigit())
async def show_ad(callback_query: CallbackQuery, state: FSMContext):
    index = int(callback_query.data) - 1
    data = await state.get_data()
    adslist = data.get("ads")

    if adslist and index < len(adslist):
        ad = adslist[index]
        await callback_query.message.edit_text(
            text=f"Ad {index+1} of {len(adslist)}\n\n<b>{index+1} - {ad[1]}</b>\n\n Description: {ad[2]}\n\n Price: ${ad[3]}",
            reply_markup=search_button(min(len(adslist), 5)),
            parse_mode=ParseMode.HTML
        )








