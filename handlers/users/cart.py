from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from keyboards.default.main import cart_markup, cats_markup
from states.shop import ShopState

@dp.message_handler(text="🛒 Savat", state="*")
async def get_cart_products(message: types.Message, state: FSMContext):
    await state.finish()
    products = db.select_user_cart(user_id=message.from_user.id)
    if products:
        text = "🛒 Savat\n\n"
        total_price = 0
        for product in products:
            mahsulot = db.select_product(id=product[-2])
            price = int(mahsulot[-2]) * product[-1]
            total_price += price
            text += f"<b>{mahsulot[1]}</b>\n{int(mahsulot[-2])} x {product[-1]} = {price}\n"
        text += f"\nUmumiy: {total_price} so'm"
        await message.answer(text=text, reply_markup=cart_markup(products))
        await ShopState.cart.set()
    else:
        await message.answer(text="Savatingiz bo'sh nimadir xarid qilasizmi?", reply_markup=cats_markup)

@dp.message_handler(text_contains="❌", state=ShopState.cart)
async def delete_cart_product(message: types.Message):
    products = db.select_user_cart(user_id=message.from_user.id)
    if products:
        del_product = message.text.split("❌")[1].strip()
        product_id = db.select_product(title=del_product)[0]
        db.clear_cart(product_id=product_id)
        await message.answer(text="Mahsulot o'chirildi", reply_markup=cart_markup(products))
    else:
        await message.answer(text="Savatingiz bo'sh nimadir xarid qilasizmi?", reply_markup=cats_markup)