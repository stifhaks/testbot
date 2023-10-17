import asyncio

from aiocryptopay import Networks, AioCryptoPay
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from unicodedata import decimal

import config
from config import testnet, cryptobot_main_net, cryptobot_test_net
from crypto import coinmarket_api, matic_help
from routs import raffle_bot_main, raffles
from routs.raffle_bot_main import mt_check_adress
from routs.routs_key import k_deposit, get_cancel_kb, get_res, db_helper, k_deposit_for, k_chose_ticket

if testnet:
	cp = AioCryptoPay(token=cryptobot_test_net, network=Networks.TEST_NET)
else:
	cp = AioCryptoPay(token=cryptobot_main_net, network=Networks.MAIN_NET)

crypto_router = Router()

class DepInf(StatesGroup):
	amount = State()
	currency = State()


# Пополнение
@crypto_router.callback_query(Text(text=k_deposit))
async def deposit(message: CallbackQuery, state: FSMContext):
	if not await mt_check_adress(message):
		return
	f_res = get_res(message)
	f_body = f_res.enter_amount
	f_response = coinmarket_api.get_matic_price()
	if f_response['code'] == 200:
		f_price = round(f_response['price'],2)
		f_body += f'1 MATIC = {f_price} USDT'
		await message.message.answer(text=f_body, reply_markup=get_cancel_kb(f_res))
		await state.set_state(DepInf.amount)
		await state.set_data(f_response)
		await message.answer()
	else:
		await message.message.answer(text='Some error, sory', reply_markup=get_cancel_kb(f_res))
		await message.answer()


s_values = ['TON','ETH','BNB','USDC','BUSD','USDT']
k_val_chose = 'chose_val'

# Запись о сумме пополнения
@crypto_router.message(DepInf.amount)
@crypto_router.callback_query(Text(startswith=k_deposit_for))
async def load_amount(message: types.Message, state: FSMContext) -> None:
	f_data = await state.get_data()
	if isinstance(message,CallbackQuery):
		callback: CallbackQuery = message
		await callback.answer()
		f_data['amount'] = float(callback.data.removeprefix(k_deposit_for))
		f_response = coinmarket_api.get_matic_price()
		if f_response['code'] != 200:
			await callback.message.answer('Что то пошло нетак, сори :(')
			return
		f_data['price'] = f_response['price']
		message = callback.message
	else:
		try:
			float(message.text)
			ok = 0
		except:
			await message.answer(text="Напишите норм число")
			return
		f_data['amount'] = float(message.text.strip())
		if f_data['amount'] <= 0.0:
			await message.answer(text="Напишите норм число")
			return

	f_kb = InlineKeyboardBuilder()
	for q_val in s_values:
		f_kb.add(InlineKeyboardButton(text=q_val,callback_data=k_val_chose+q_val))
	f_kb.adjust(3)

	await message.answer(text='Выберите валюту для пополнения',
											 reply_markup=f_kb.as_markup(resize_keyboard=True))
	await state.set_state(DepInf.currency)
	await state.set_data(f_data)




# Запись валюты для пополнения
@crypto_router.callback_query(Text(startswith=k_val_chose))
async def load_currency(message: CallbackQuery, state: FSMContext, bot: Bot) -> None:
	f_data = await state.get_data()
	await message.answer()
	f_val = message.data.removeprefix(k_val_chose)
	# if str(f_data['currency']) == k_cancel:
	# 	await state.clear()
	# 	await start(message)
	# 	return
	# await message.answer(text=f"Вы получаете 💰 {f_data['amount']} {curency}, оплачиваете 💳 {f_data['currency']}")
	# await state.clear()
	await payment(cur=f_val, amount=f_data['amount'], message=message, bot = bot, price=f_data['price'], state=state)


# Создание и проверка офера на пополнение
async def payment(cur, amount, message, bot, price,state: FSMContext):
	counter = 0
	rates = await cp.get_exchange_rates()

	matic_price = price
	usdt_amount_in_rub = amount * matic_price * rates[0].rate
	# ton_amount = ton_amount + round(ton_amount * s_comis,2)
	cur_price = 0
	match cur:
		case ("USDT"):
			cur_price = rates[0].rate
		case ("TON"):
			cur_price = rates[18].rate
		case ("ETH"):
			cur_price = rates[54].rate
		case ("BNB"):
			cur_price = rates[72].rate
		case ("BUSD"):
			cur_price = rates[90].rate
		case ("USDC"):
			cur_price = rates[108].rate

	price = usdt_amount_in_rub / cur_price
	non_sience = str(price).split('e')
	non_s_price = round(float(non_sience[0]),6)
	non_s_e = int(non_sience[1])
	for i in range(0,abs(non_s_e)):
		if non_s_e<0:
			non_s_price = non_s_price / 10
		else:
			non_s_price *= 10

	# price = round(price,8)
	# price = str(price)
	f_price_str = '{:8f}'.format(price)
	f_body = f"Вы получаете 💰 {amount} MATIC , оплачиваете {f_price_str} 💳 {cur}\n\n" \
					 f"У Вас будет 1 час для оплаты чека, после чего он будет закрыт\n\n" \
					 f"⬇️ Ссылка на оплату ⬇️:"
	try:
		invoice = await cp.create_invoice(asset=cur, amount=price)
	except Exception as e:
		print(e)
		await bot.send_message(chat_id=message.from_user.id, text=f"{price} {cur} - слишком маленькая сумма для пополнения\n"
																															f"попробуйте в другой валюте")
	dep_ikb = InlineKeyboardBuilder()
	dep_ikb1 = InlineKeyboardButton(text=f"Пополнить баланс на {amount} ", url=invoice.pay_url)
	dep_ikb.add(dep_ikb1)
	await bot.send_message(chat_id=message.from_user.id, text=f_body, reply_markup=dep_ikb.as_markup())
	# await bot.send_message(chat_id=message.chat.id, text="У Вас будет 1 час для оплаты чека, после чего он будет закрыт")
	ыщьумфд = 666.3453
	safdsf = [666, 12434]

	while counter <= 360:
		invoices = await cp.get_invoices(invoice_ids=invoice.invoice_id)
		if invoices.status == 'paid':
			await bot.send_message(chat_id=message.from_user.id, text="Оплата прошла успешно")
			db_helper.add_records(message.from_user.id, "+", amount)
			if matic_help.send_matic(amount,message.from_user.id):
				await bot.send_message(chat_id=message.from_user.id, text=f"Перевод {amount} MATIC прошел")
				f_data = await state.get_data()
				if k_chose_ticket in f_data:
					await raffles.mt_join_to_rafle_msg(f_data[k_chose_ticket],bot,message)
					return
			else:
				await bot.send_message(chat_id=message.from_user.id, text=f"Ошибка перевода :(")
			return await raffle_bot_main.process_start_command(message)
		if invoices.status == 'expired':
			await bot.send_message(chat_id=message.from_user.id, text="Срок дайствия инвойса истек")
		counter += 1
		await asyncio.sleep(10)
