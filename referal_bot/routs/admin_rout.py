import os
import shutil

from aiogram import Router, F, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery


from tools import tools

from referal_bot import bonus_script
from referal_bot.key_store import k_balances, k_static, s_rer_data, SUCCSESS
from referal_bot.midlew.admin_midlew import AdminMessageMidleware

admin_router = Router()
admin_router.message.filter(F.chat.type == "private")
admin_router.message.middleware(AdminMessageMidleware())

class Form(StatesGroup):
	home = State()

@admin_router.message(Command('help'))
async def mt_clear(message: types.Message, state: FSMContext):
	await message.answer('/clear - очистить данные рефералов\n'
											 f'/{k_balances} - балансы кошельков\n'
											 f'/{k_static} - статистика\n'
											 '/deposit - пополнить баланс\n')

@admin_router.message(Command('clear'))
async def mt_clear(message: types.Message, state: FSMContext):
	shutil.rmtree('data')
	tools.makedir(tools.k_data)
	bonus_script.init_data()
	await message.answer('Данные очищены')
k_cancel = 'cancel'
@admin_router.message(Command('deposit'))
async def mt_depos(message: types.Message, state: FSMContext):
	await state.set_state(Form.home)

	buttons = [
		[
			types.InlineKeyboardButton(
				text='Отмена',
				callback_data=k_cancel)]
	]

	keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)

	await message.answer('Введите сумму в TON',reply_markup=keyboard)

@admin_router.callback_query(Text(text=k_cancel))
async def mt_cancel(query: CallbackQuery, state: FSMContext):
	await state.clear()
	await query.answer()
	await query.message.answer('Отменено')


@admin_router.message(Command(k_balances))
async def mt_balansec(message: types.Message, state: FSMContext):
	f_balances = bonus_script.status()
	f_body = 'Балансы:\n\n'
	for q_b in f_balances:
		f_body += f'{q_b["currency_code"]}: {q_b["available"]}\n'
	await message.answer(f_body)

@admin_router.message(Command(k_static))
async def mt_status(message: types.Message, state: FSMContext):
	f_list = os.listdir(tools.tools.k_data+s_rer_data)
	f_body = 'Статистика рефереров:\n\n'
	for q_rer in f_list:
		f_body += q_rer
		q_rer = tools.tools.get_data(s_rer_data+q_rer)
		q_referals = q_rer.keys()
		q_count = 0
		for q_ref in q_referals:
			if q_rer[q_ref]['stats'] == SUCCSESS:
				q_count += 1
		f_body += f' - {q_count} реферал(ы/ов)\n'

	await message.answer(f_body)
