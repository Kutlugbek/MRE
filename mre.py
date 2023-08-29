import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class Form(StatesGroup):
	name = State()

key_menu_o = [[KeyboardButton(text='Продукты')]]
keyboard_menu_o = ReplyKeyboardMarkup(keyboard=key_menu_o, resize_keyboard=True)

product_kb = InlineKeyboardBuilder()
product_kb.add(InlineKeyboardButton(text='Add product', callback_data='add_product'))

@router.message(Command('start'))
async def start_message(message: Message):
	if message.from_user.id:
		await message.answer(text='Hello', reply_markup=keyboard_menu_o)



@router.message(F.text)
async def message_f(message: Message, bot: Bot):
	if message.text == 'Продукты':
		await message.answer(text='Choose', reply_markup=product_kb.as_markup())



@router.callback_query(F.data)
async def data_filter(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
	if callback.data == 'add_product':
		await state.set_state(Form.name)
		print('This print works')


@router.message(Form.name)
async def name_product(message: Message, state: FSMContext):
	if message.text:
		print('This print is not working')


async def main():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token='TOKEN')
	dp = Dispatcher(storage=MemoryStorage())
	dp.include_router(router)
	await dp.start_polling(bot)

if __name__ == '__main__':
	try:
		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		pass