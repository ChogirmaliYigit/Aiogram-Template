from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    category = State()
    secondary_cat = State()
    product = State()
    amount = State()
    cart = State()

