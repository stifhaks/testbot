import asyncio
import os

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, Text, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils.keyboard import InlineKeyboardBuilder



import private_key
from referal_bot import bonus_script

bot = Bot(token=private_key.s_target_token)
dp = Dispatcher()

def getBot():
	return bot

from midlewares.some_mid import WeekendMessageMiddleware, WeekendCallbackMiddleware

form_router = Router()
form_router.message.filter(F.chat.type == "private")
form_router.message.middleware(WeekendMessageMiddleware())

form_router.callback_query.middleware(WeekendCallbackMiddleware())


class Form(StatesGroup):
	home = State()


k_back = 'back_clb'

s_target = ''

@dp.message(Command('start'))
@dp.message(lambda message: message.text == k_back)
@dp.callback_query(Text(text=k_back))
async def process_start_command(message: types.Message,command: CommandObject, state: FSMContext):

	f_user_id = str(message.from_user.id)

	f_args = command.args
	f_body = 'Добро пожаловать в нашего бота :)'
	if f_args:
		f_refr_id = f_args

		await bonus_script.send_bonus(f_refr_id,f_user_id)


	await message.reply(f_body)




@form_router.message(Text(startswith=''))
async def process_chat_ai_message(message: types.Message, state: FSMContext):
	await message.answer('ok')


async def main():
	dp.include_router(form_router)
	print('main run')
	f_me = await bot.get_me()
	print(f'bot run on @{f_me.username}')
	await dp.start_polling(bot)
	print(f'{f_me.username} finished :((')


def init():
	# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	f_looper = asyncio.get_event_loop()
	print('init run')

	f_looper.run_until_complete(
		asyncio.get_event_loop().create_task(main()))
	print('fin run')


if __name__ == "__main__":
	init()