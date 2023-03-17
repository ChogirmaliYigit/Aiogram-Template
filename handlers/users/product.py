from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from keyboards.default.main import products_markup, amount_markup, cats_markup, secondary_cart_markup
from states.shop import ShopState



@dp.message_handler(state=ShopState.secondary_cat)
async def get_products(message: types.Message, state: FSMContext):
    secondary_cat = db.select_secondary_cat(title=message.text)
    await state.update_data({"secondary_cat": secondary_cat})
    if secondary_cat:
        await message.answer(text="Mahsulotni tanlang", reply_markup=products_markup(secondary_cat=secondary_cat))
        await ShopState.product.set()
    else:
        await message.answer("Hozircha bu kategoriyada mahsulot yo'q")

@dp.message_handler(text="⬅️ Orqaga", state=ShopState.product)
async def goto_products(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cats = data.get("cats")
    await message.answer(text="Kategoriyani tanlang", reply_markup=secondary_cart_markup(cats=cats))
    await ShopState.secondary_cat.set()

@dp.message_handler(state=ShopState.product)
async def get_amount(message: types.Message, state: FSMContext):
    product = db.select_product(title=message.text)
    await state.update_data({"product_id": product[0]})
    await message.answer_photo(photo=product[-3], caption=f"{product[1]}\n\n{product[2]}\n\nNarxi: {product[-2]}")
    await message.answer(text="Miqdorini <b>tanlang</b> yoki <b>kiriting</b>", reply_markup=amount_markup)
    await ShopState.amount.set()

@dp.message_handler(text="⬅️ Orqaga", state=ShopState.amount)
async def goto_products(message: types.Message, state: FSMContext):
    data = await state.get_data()
    secondary_cat = data.get("secondary_cat")
    await message.answer(text="Mahsulotni tanlang", reply_markup=products_markup(secondary_cat=secondary_cat))
    await ShopState.product.set()

@dp.message_handler(state=ShopState.amount)
async def add_product_to_cart(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    if message.text.isdigit() and int(message.text) > 0:
        quantity = int(message.text)
        product = db.select_user_cart(user_id=message.from_user.id, product_id=product_id)[0]
        if product:
            quantity += product[-1]
            db.update_user_cart(user_id=message.from_user.id, product_id=product_id, quantity=quantity)
        else:
            db.add_cart(user_id=message.from_user.id, product_id=product_id, quantity=quantity)
        await message.answer(text="Mahsulot savatchaga qo'shildi, davom etamizmi?", reply_markup=cats_markup)
        await ShopState.category.set()
    else:
        await message.answer(text="Miqdorini <b>tanlang</b> yoki <b>kiriting</b>", reply_markup=amount_markup)


