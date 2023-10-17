

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, Text, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hide_link

import key_store
from crypto import fkin_key_generator
from database.db_keys import user_table, k_user_id, k_locate, k_login, k_key, k_addres

from midlewares.some_mid import WeekendMessageMiddleware, WeekendCallbackMiddleware
from referal_bot import bonus_script
from res import ru_res, ua_res, def_res
from res.def_res import DefRess
from routs.routs_key import k_promo, get_res, db_helper, k_ru_key, k_ukr_key, k_raffles, k_back, k_deposit, k_category, \
    get_cancel_btn


form_router = Router()
form_router.message.filter(F.chat.type == "private")
form_router.message.middleware(WeekendMessageMiddleware())

form_router.callback_query.middleware(WeekendCallbackMiddleware())




class Form(StatesGroup):
    home = State()
    input_adress = State()

@form_router.message(Command('start'))
@form_router.message(lambda message: message.text == k_back)
@form_router.callback_query(Text(text=k_back))
async def process_start_command(message: types.Message,command: CommandObject = 0,state: FSMContext = 0):
    print(f'start with {message.from_user.id}')
    if not state == 0:
        await state.set_data({})

    if command != 0:
        f_args = command.args

        if f_args:
          f_refr_id = f_args
          await bonus_script.send_bonus(f_refr_id, message.from_user.id)



    if not await mt_check_auth(message):
        return
    f_res = get_res(message)

    if isinstance(message, types.CallbackQuery):
        await message.answer()
        message = message.message
    # print(f'cont with {message.from_user.id}')
    # f'{f_res.go_to_promo}
    kb_build = InlineKeyboardBuilder()
    kb_build.row(InlineKeyboardButton(text=f_res.promo_btn,
                                      url='https://raffle.markets/promo-raffle'))
    kb_build.row(InlineKeyboardButton(text=f_res.category,
                                      callback_data=k_category))
    kb_build.row(InlineKeyboardButton(text=f_res.raffle_btn,
                                      callback_data=k_raffles))
    kb_build.row(InlineKeyboardButton(text=f_res.about_btn,
                                      url=key_store.s_about_link))
    kb_build.row(InlineKeyboardButton(text=f_res.deposit_btn,
                                      callback_data=k_deposit))
    kb_build.row(InlineKeyboardButton(text=f_res.my_adress,
                                      callback_data=k_my_adress))



    await message.answer(f_res.greetings, reply_markup=kb_build.as_markup(resize_keyboard = True))

k_input_adres = 'input_adres'
k_my_adress = 'my_adress'
k_change_adress = 'change_adress'

@form_router.callback_query(Text(text=k_my_adress))
async def clb_request_wallet(query: CallbackQuery,state: FSMContext):
    f_res = get_res(query)
    f_adress = db_helper.get_cell(user_table, k_addres, query.from_user.id)

    kb_build = InlineKeyboardBuilder()
    kb_build.row(InlineKeyboardButton(text=f_res.change_adress,
                                      callback_data=k_change_adress))
    await query.answer()
    await query.message.answer(f'{f_res.your_adress} \n'
                               f'0x{f_adress}',reply_markup=kb_build.as_markup(resize_keyboard = True))

@form_router.callback_query(Text(text=k_change_adress))
async def clb_request_wallet(query: CallbackQuery,state: FSMContext):
    f_res = get_res(query)
    await mt_request_wallet(f_res, query)

async def mt_check_adress(message: Message):
    f_user_id = (message.from_user.id)
    f_res = get_res(message)
    if not db_helper.cell_exist(user_table, f_user_id,k_addres):
        await mt_request_wallet(f_res,message)
        return False
    return True

async def mt_request_wallet(f_res: DefRess,query: CallbackQuery):
    f_body = f'{f_res.request_wallet1}+https://metamask.io/ \n\n'
    f_body += f_res.request_wallet2
    kb_build = InlineKeyboardBuilder()
    kb_build.row(InlineKeyboardButton(text=f_res.send_adress,
                                      callback_data=k_input_adres))
    kb_build.row(get_cancel_btn(f_res))
    await query.message.answer(f_body,reply_markup=kb_build.as_markup(resize_keyboard=True))
    await query.answer()

@form_router.callback_query(Text(text=k_input_adres))
async def clb_request_wallet(query: CallbackQuery,state: FSMContext):
    f_res = get_res(query)
    kb_build = InlineKeyboardBuilder()
    kb_build.row(get_cancel_btn(f_res))
    await state.set_state(Form.input_adress)
    await query.message.answer(f_res.enter_adress, reply_markup=kb_build.as_markup(resize_keyboard=True))
    await query.answer()

@form_router.message(Form.input_adress)
async def mt_input_adress_form(message: types.Message,state: FSMContext):
    f_adress = message.text
    f_res = get_res(message)

    kb_build = InlineKeyboardBuilder()
    kb_build.row(get_cancel_btn(f_res))
    if not f_adress.startswith('0x'):
        await message.answer('Пришлите правильный адрес',reply_markup=kb_build.as_markup(resize_keyboard=True))
        return
    await state.clear()
    db_helper.add_cell(user_table,message.from_user.id,k_addres,f_adress)
    kb_build = InlineKeyboardBuilder()
    kb_build.row(InlineKeyboardButton(text=f_res.main,
                                      callback_data=k_back))
    await message.answer('Адрес добавлен',reply_markup=kb_build.as_markup(resize_keyboard=True))

async def mt_check_auth(message: types.Message):
    f_user_id = str(message.from_user.id)
    if not db_helper.row_exist(user_table, f_user_id):
        await mt_chose_locate(message)
        return False
    return True

s_langs = [{'t':ru_res.RuRes.name,'c':k_ru_key},
           {'t':ua_res.UaRes.name,'c':k_ukr_key}]
k_lang_prefix = 'lang_'


async def mt_chose_locate(message: types.Message):
    f_user_id = str(message.from_user.id)
    f_img = 'https://cdn.iz.ru/sites/default/files/styles/900x506/public/article-2018-02/20150418_gaf_uw7_019.jpg?itok=EZ6G4vke'
    kb_build = InlineKeyboardBuilder()
    for q_l in s_langs:
        kb_build.add(InlineKeyboardButton(text=q_l['t'],
                                          callback_data=k_lang_prefix + q_l['c']))
    f_body = f'{hide_link(f_img)}' \
             f'ЧЕЙ КРЫМ???'
    if message is CallbackQuery:
        await message.message.answer(f_body, reply_markup=kb_build.as_markup(resize_keyboard=True),
                                     parse_mode="HTML")
        await message.answer()
    else:
        await message.answer(f_body,reply_markup=kb_build.as_markup(resize_keyboard = True),
                             parse_mode="HTML")

@form_router.callback_query(Text(startswith=k_lang_prefix))
async def mt_set_local(callback: CallbackQuery,state: FSMContext):
    f_local = callback.data.removeprefix(k_lang_prefix)
    f_user_id = str(callback.from_user.id)
    f_nik = callback.from_user.username
    if not f_nik:
        f_nik = f_user_id

    f_key, f_adres = fkin_key_generator.getNewKey()
    db_helper.add_row(user_table,{
        k_locate: f_local,
        k_user_id: f_user_id,
        k_login: f_nik,
        # k_key: f_key,
        # k_addres: f_adres
    })
    await callback.answer()

    await process_start_command(callback,state)



# @form_router.message(Text(startswith=''))
# async def process_chat_ai_message(message: types.Message, state: FSMContext):
#     await message.answer('ok')


