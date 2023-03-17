from aiogram import types
from loader import dp
from keyboards.default.main import cats_markup
from states.shop import ShopState


@dp.message_handler(text="🛍 Buyurtma berish")
async def bot_echo(message: types.Message):
    await message.answer(text="Nimadan boshlaymiz?", reply_markup=cats_markup)
    await ShopState.category.set()

