import asyncio
import os
import shutil

import tools.tools
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

import private_key
from referal_bot import bonus_script
from referal_bot.config import bonus_bot_token
from referal_bot.key_store import k_create_link, k_stats, s_rer_data, s_ref_data, DENIED, SUCCSESS
from referal_bot.routs.admin_rout import admin_router

bot = Bot(token=bonus_bot_token)

def getBot():
	return bot
dp = Dispatcher()

from midlewares.some_mid import WeekendMessageMiddleware, WeekendCallbackMiddleware

form_router = Router()
form_router.message.filter(F.chat.type == "private")
form_router.message.middleware(WeekendMessageMiddleware())
form_router.callback_query.middleware(WeekendCallbackMiddleware())





class Form(StatesGroup):
	home = State()


k_back = 'back_clb'
k_check_stackd_bonus = 'check_stack'

s_target = 'https://t.me/test3_omgbot'

@dp.message(Command('start'))
@dp.message(lambda message: message.text == k_back)
@dp.callback_query(Text(text=k_back))
async def process_start_command(message: types.Message, state: FSMContext):

	await state.clear()
	f_user_id = str(message.from_user.id)
	f_nik = message.from_user.username
	if not f_nik:
		f_nik = f_user_id
	f_user_data = {'nic': f_nik}

	if isinstance(message, types.CallbackQuery):
		await message.answer()
		message = message.message
	print(f'cont with {message.from_user.id}')

	buttons = [
		[
			types.InlineKeyboardButton(
				text='Создать реферальную ссылку',
				callback_data=k_create_link)],
		[
			types.InlineKeyboardButton(
				text='Статистика',
				callback_data=k_stats)],
		[
			types.InlineKeyboardButton(
				text='Получить застрявшие бонусы',
				callback_data=k_check_stackd_bonus)]
	]

	keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)

	f_body = f'Бот сгенерирует реферальную ссылку на таргет бота {s_target}, ' \
					 f'по которой можно будет получать вознаграждение вам, и каждому перешедшему по ссылке!'

	await message.reply(f_body, reply_markup=keyboard)




@dp.message(Form.home)
async def mt_get_voice(message: types.Message, state: FSMContext):
	f_amount = message.text
	if not f_amount.isdigit():
		await message.answer('Надо ввести целое число')
		return

	await state.clear()
	f_link = bonus_script.make_invoice(int(f_amount))
	await message.answer(f_link)

@form_router.callback_query(Text(text=k_stats))
async def mt_statistic(query: CallbackQuery):
	f_id = str(query.from_user.id)
	f_path = s_rer_data + f_id
	f_data = tools.tools.get_data(f_path)
	if f_data != 404:
		f_size = len(f_data.keys())
		await query.message.answer(f'Всего переходов по вашей ссылке: {f_size} \n'
															 f'Вы заработали {f_size * config.k_bonus_size} TON')
	else:
		await query.message.answer('По вашей ссылке пока не было переходов')
	await query.answer()


@form_router.callback_query(Text(text=k_check_stackd_bonus))
async def mt_check_stackt(query: CallbackQuery):
	f_id = str(query.from_user.id)

	f_list = os.listdir(tools.tools.k_data+s_ref_data)
	f_list2 = os.listdir(tools.tools.k_data+s_rer_data)
	f_path = ''
	if f_id in f_list:
		f_path = s_ref_data + f_id
		f_data = tools.tools.get_data(f_path)

		if f_data[k_stats] == DENIED:
			await query.message.answer('Найден застрявший платеж.\n\n'
																 'Сейчас повторим..')
			await query.answer()
			if await bonus_script.send_repeat_trans(f_id,query):
				f_data[k_stats] = SUCCSESS
				tools.tools.set_data(f_path,f_data)
				return


	elif f_id in f_list2:
		f_path = s_rer_data + f_id
		f_data = tools.tools.get_data(f_path)
		for q_ref in f_data.keys():
			q_ref_data = f_data[q_ref]
			if q_ref_data[k_stats] == DENIED:
				await query.message.answer('Найден застрявший платеж.\n\n'
																	 'Сейчас повторим..')
				await query.answer()
				if await bonus_script.send_repeat_trans(f_id, query):
					f_data[q_ref][k_stats] = SUCCSESS
					tools.tools.set_data(f_path,f_data)
				await asyncio.sleep(0.5)


	else:
		await query.message.answer('Не найдено застрявших платежей')
		await query.answer()
		return



	await query.message.answer('Не найдено застрявших платежей')
	await query.answer()


@form_router.callback_query(Text(text=k_create_link))
async def mt_create_link(query: CallbackQuery):

	f_id = str(query.from_user.id)
	f_nik = query.from_user.username
	f_nik = f_nik if f_nik else f_id
	f_link = f'{s_target}?start={f_id}'

	await query.answer()
	await query.message.answer(f'Вот ваша реферальная ссылка: {f_link}')

@form_router.message(Text(startswith=''))
async def process_chat_ai_message(message: types.Message, state: FSMContext):
	await message.answer('ok')
	await state.clear()


async def mt_send_to_admin(f_body):
	for q_a in config.s_admins:
		await bot.send_message(q_a,f_body)

async def main():
	dp.include_router(admin_router)
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