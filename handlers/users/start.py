import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    if not name.startswith('<') and not name.endswith('>'):
        # Foydalanuvchini bazaga qo'shamiz
        try:
            db.add_user(id=message.from_user.id, name=name)
            await message.answer(f"Xush kelibsiz! {name}")
            # Adminga xabar beramiz
            count = db.count_users()[0]
            msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS[0], text=msg)

        except sqlite3.IntegrityError as err:
            await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
            await message.answer(f"Xush kelibsiz! {name}")

        except Exception as err:
            await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
            await message.answer(f"Xush kelibsiz! {name}")

    else:
        if message.from_user.username:
            try:
                db.add_user(id=message.from_user.id, name=name)
                msg = f"@{message.from_user.username} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
                await bot.send_message(chat_id=ADMINS[0], text=msg)
                await message.answer(f"Xush kelibsiz! @{message.from_user.username}")

            except sqlite3.IntegrityError as err:
                await bot.send_message(chat_id=ADMINS[0], text=f"@{message.from_user.username} bazaga oldin qo'shilgan")
                await message.answer(f"Xush kelibsiz! @{message.from_user.username}")
            
            except Exception as err:
                await bot.send_message(chat_id=ADMINS[0], text=f"@{message.from_user.username} bazaga oldin qo'shilgan")
                await message.answer(f"Xush kelibsiz! @{message.from_user.username}")

        else:
            try:
                db.add_user(id=message.from_user.id, name=name)
                msg = f"{message.from_user.id} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
                await bot.send_message(chat_id=ADMINS[0], text=msg)
                await message.answer(f"Xush kelibsiz!")

            except sqlite3.IntegrityError as err:
                await bot.send_message(chat_id=ADMINS[0], text=f"{message.from_user.id} bazaga oldin qo'shilgan")
                await message.answer(f"Xush kelibsiz!")
            
            except Exception as err:
                await bot.send_message(chat_id=ADMINS[0], text=f"{message.from_user.id} bazaga oldin qo'shilgan")
                await message.answer(f"Xush kelibsiz!")
