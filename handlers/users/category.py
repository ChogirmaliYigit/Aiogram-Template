from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from keyboards.default.main import secondary_cart_markup, cats_markup, main_markup
from states.shop import ShopState

@dp.message_handler(text="🏠 Bosh menyu", state="*")
async def goto_products(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="🏠 Bosh sahifa", reply_markup=main_markup)

@dp.message_handler(text="⬅️ Orqaga", state=ShopState.secondary_cat)
async def goto_products(message: types.Message, state: FSMContext):
    await message.answer(text="Bo'limni tanlang", reply_markup=cats_markup)
    await ShopState.category.set()

@dp.message_handler(text="⬅️ Orqaga", state=ShopState.category)
async def goto_products(message: types.Message, state: FSMContext):
    await message.answer(text="🏠 Bosh sahifa", reply_markup=main_markup)
    await state.finish()

@dp.message_handler(state=ShopState.category)
async def get_secondary_cats(message: types.Message, state: FSMContext):
    cats = db.select_cat(title=message.text)
    await state.update_data({"cats": cats})
    if cats:
        await message.answer(text="Kategoriyani tanlang", reply_markup=secondary_cart_markup(cats=cats))
        await ShopState.secondary_cat.set()
    else:
        await message.answer(text="Hozircha bu kategoriyada mahsulot yo'q")

