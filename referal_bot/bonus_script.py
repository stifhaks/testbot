import datetime
import json

import requests
import tools.tools
from aiogram.types import Message, CallbackQuery

from referal_bot import config
from referal_bot.config import TESTNET, k_bonus_size, s_test_token, s_main_token
from referal_bot.key_store import s_ref_data, s_rer_data, k_stats, DENIED, SUCCSESS
from referal_bot.routs import main_ref_bot

from routs import init_rout as main_targ_bot



s_test_endpoint = 'https://testnet-pay.crypt.bot/api/'
s_test_crypto = 'TRX'
s_test_market = '@CryptoTestnetBot'

s_main_endpoint = 'https://pay.crypt.bot/api/'
s_main_crypto = 'TON'
s_main_market = '@CryptoBot'

def init_data():
	tools.tools.makedir(tools.tools.k_data + s_ref_data)
	tools.tools.makedir(tools.tools.k_data + s_rer_data)

init_data()


async def send_bonus(referer,referal):

	if TESTNET:
		f_cryp = s_test_crypto
		f_market = s_test_market
	else:
		f_cryp = s_main_crypto
		f_market = s_main_market

	if referal == referer:
		bot = main_targ_bot.getBot()
		f_body = f'Нельзя получить награду по собственной ссылке'
		await bot.send_message(referal, f_body)
		return

	f_data = tools.tools.get_data(s_ref_data+str(referal))
	if f_data != 404:
		bot = main_targ_bot.getBot()
		ref_bot = main_ref_bot.getBot()
		f_bot_nik = await ref_bot.get_me()
		if f_data[k_stats] == DENIED:
			f_body = f'Вам полагается бонус за вход по реферальной ссылке\n\n' \
							 f'НО  ВАШ КОШЕЛЕК НЕ НАЙДЕТ НА {f_market} !!\n\n' \
							 f'Стартаните {f_market} Чтобы получать вознаграждения!!!!\n' \
							 f'Затем обязательно перейдите в @{f_bot_nik.username} ' \
							 f'и проверьте свои вознаграждения'
			await bot.send_message(referal, f_body)
			return
		else:
			f_body = f'Вы уже получили свое вознаграждение'
			await bot.send_message(referal, f_body)
			return
	else:
		f_data = {'referer': referer}

	f_rer_data = tools.tools.get_data(s_rer_data + str(referer))
	if f_rer_data != 404:
		f_rer_data[referal] = {}
	else:
		f_rer_data = {referal: {}}
	f_rout = 'transfer'



	f_res = await send_trans(referer,f_cryp)
	if f_res == 'USER_NOT_FOUND':
		f_rer_data[referal][k_stats] = DENIED
		tools.tools.set_data(s_rer_data + str(referer),f_rer_data)
		bot = main_ref_bot.getBot()
		f_bot_nik = await bot.get_me()
		f_body = f'пользователь {referal} воспользовался вашей реферальной ссылкой!\n\n' \
						 f'НО  ВАШ КОШЕЛЕК НЕ НАЙДЕТ НА {f_market} !!\n\n' \
						 f'Стартаните {f_market} Чтобы получать вознаграждения!!!!\n' \
						 f'Затем обязательно перейдите в @{f_bot_nik.username} ' \
						 f'и проверьте свои вознаграждения'
		await bot.send_message(referer, f_body)
	elif f_res:
		f_rer_data[referal][k_stats] = SUCCSESS
		tools.tools.set_data(s_rer_data + str(referer), f_rer_data)
		bot = main_ref_bot.getBot()
		f_body = f'пользователь {referal} воспользовался вашей реферальной ссылкой!\n\n' \
						 f'Вам уже отправлено вознаграждение {k_bonus_size} {f_cryp} в {f_market}!'
		await bot.send_message(referer,f_body)
	else:
		f_rer_data[referal][k_stats] = DENIED
		tools.tools.set_data(s_rer_data + str(referer), f_rer_data)


	f_res2 = await send_trans(referal,f_cryp)
	if f_res2 == 'USER_NOT_FOUND':
		f_data[k_stats] = DENIED
		tools.tools.set_data(s_ref_data + str(referal), f_data)

		bot = main_targ_bot.getBot()
		ref_bot = main_ref_bot.getBot()
		f_bot_nik = await ref_bot.get_me()
		f_body = f'Вам полагается бонус за вход по реферальной ссылке\n\n' \
						 f'НО  ВАШ КОШЕЛЕК НЕ НАЙДЕТ НА {f_market} !!\n\n' \
						 f'Стартаните {f_market} Чтобы получать вознаграждения!!!!\n' \
						 f'Затем обязательно перейдите в @{f_bot_nik.username} ' \
						 f'и проверьте свои вознаграждения'
		await bot.send_message(referal, f_body)
	elif f_res2:
		f_data[k_stats] = SUCCSESS
		tools.tools.set_data(s_ref_data + str(referal), f_data)
		bot = main_targ_bot.getBot()
		f_body = 'Добро пожаловать в нашего бота :)\n\n' \
						 f'Вы были приглашены пользователем партнером, и получаете бонусные' \
						 f' {k_bonus_size} TON!\n\n' \
						 f'Бонус уже отправлен на ваш кошелек {f_market}'
		await bot.send_message(referal, f_body)
		return True
	else:
		f_data[k_stats] = DENIED
		tools.tools.set_data(s_ref_data + str(referal), f_data)

async def send_repeat_trans(f_id,query : CallbackQuery):
	if TESTNET:
		f_cryp = s_test_crypto
	else:
		f_cryp = s_main_crypto

	f_res = await send_trans(f_id, f_cryp)
	if f_res == 'USER_NOT_FOUND':
		await query.message.answer('Кошелек до сих пор не создан..')
		return False
	elif f_res:
		await query.message.answer('Платеж проведен!')
		await query.answer()

		return True
	else:
		await query.message.answer('Какая то ошибка :(\n\n'
												 'Мы уже разбираемся с этим')
	await query.answer()
	return False




def send_trans_sync(f_id):
	f_rout = 'transfer'

	if TESTNET:
		f_cryp = s_test_crypto
	else:
		f_cryp = s_main_crypto

	f_param1 = {
		'user_id': f_id,
		'asset': f_cryp,
		'amount': config.k_bonus_size,
		'spend_id': str(datetime.datetime.now().timestamp())
	}
	f_msg, f_code = req_api(f_rout, f_param1)
	return f_msg, f_code

async def send_trans(f_id,f_cryp):
	f_market = s_test_market if TESTNET else s_main_market


	f_msg, f_code = send_trans_sync(f_id)
	if f_code == 200:

		return True
	elif f_msg == 'INSUFFICIENT_FUNDS':
		print('CryptoBot ERROR: ' + f_msg)
		await main_ref_bot.mt_send_to_admin(f'Баланс {f_cryp} {f_market} кончился, переводы не проходят!!')
	elif f_msg == 'USER_NOT_FOUND':
		return f_msg
	else:
		print('CryptoBot ERROR: ' + f_msg)
		await main_ref_bot.mt_send_to_admin(f'ОШИБКА КРИПТОБОТА!!!!:\n\n' +
																				f_msg)

def req_api(f_rout,f_params):
	if TESTNET:
		m_endp = s_test_endpoint
		m_token = s_test_token
	else:
		m_endp = s_main_endpoint
		m_token = s_main_token

	f_head = {'Crypto-Pay-API-Token': m_token}

	f_res = requests.get(m_endp+f_rout, headers=f_head,params=f_params)
	f_json = json.loads(f_res.text)
	f_code = f_res.status_code
	if f_code == 200:
		f_msg = f_json['result']
	else:
		f_msg = f_json['error']['name']
	#'INSUFFICIENT_FUNDS'
	# TODO недостаточно средств!!
	return f_msg,f_code

def make_invoice(amount):

	if TESTNET:
		f_cryp = s_test_crypto
	else:
		f_cryp = s_main_crypto

	f_api = 'createInvoice'
	f_param = {
		'asset': f_cryp,
		'amount': amount,
	}

	f_msg,f_code = req_api(f_api,f_param)
	f_link = f_msg['pay_url']
	print(f_msg)
	return f_link

def status():
	f_res,f_code = req_api('getBalance',{})
	print(f_res)
	return f_res


f_param1 = {
		'user_id': '6098261433',
		'asset': 'TON',
		'amount': config.k_bonus_size,
		'spend_id': str(datetime.datetime.now().timestamp())
	}

f_rout = 'transfer'
if __name__ == "__main__":
	send_trans_sync(6053798576)