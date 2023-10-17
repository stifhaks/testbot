from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import database
from res import def_res, ru_res, ua_res

k_promo = 'promo'
k_raffles = 'raffles'
k_back = 'back_clb'
k_deposit = 'deposit'
k_deposit_for = 'dep_for_'
k_category = 'category'
k_chose_ticket = 'chose_ticket'



k_ru_key = 'rus'
k_ukr_key = 'ukr'

db_helper = database.db_helper.db('bot_data.db')
s_res = {
    k_ru_key: ru_res.RuRes(),
    k_ukr_key: ua_res.UaRes()
}

def get_res(message):
    f_user_id = str(message.from_user.id)
    f_loc = db_helper.get_used_locate(f_user_id)
    f_res: def_res.DefRess = s_res[f_loc]
    return f_res

def get_cancel_btn(f_res: def_res.DefRess):
    return InlineKeyboardButton(text=f_res.cancel,
                         callback_data=k_back)

def get_cancel_kb(f_res):
    return InlineKeyboardBuilder().add(get_cancel_btn(f_res))

