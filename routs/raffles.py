import datetime

from aiogram import Router, types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hide_link
from web3 import Web3

import config
from crypto import graph_help
from res.def_res import DefRess
from routs.raffle_bot_main import mt_check_adress
from routs.routs_key import k_promo, get_res, get_cancel_btn, k_raffles, k_category, k_deposit, k_deposit_for, \
  k_chose_ticket

raf_rout = Router()

k_join_ref = 'join_ref_'
k_next = 'next'
k_prev = 'prev'
k_page = 'page'
k_msg_list = 'msg_list'
k_category_chose = 'cat_'
s_category_list = ['All',
                  'Collectible',
                  'Home',
                  '👠 Fashion 👠',
                  '🍩 Food 🍩',
                  'Health',
                  '💍 Jwellery 💍',
                  'Miscellaneous',
                  'Realty',
                  '⚽️ Sports ⚽️',
                  '💻 Tech 💻',
                  '🏎 Vehicles 🏎']


class Form(StatesGroup):
  idle = State()
  input_ticket = State()

def mt_get_raffle_body(f_data):
  q_stages = f_data['stages']
  q_cur_stage = 0
  if len(q_stages) > 1:
    q_cur_stage = next(x for x in q_stages if x['stageType'] == f_data['ongoingStage'])
  else:
    q_cur_stage = q_stages[0]
  q_img = f_data["images"]
  q_time = int(f_data['createdAt'])
  q_time = q_time + int(f_data['raffleEndTime'])
  q_date = datetime.datetime.fromtimestamp(int(q_time))

  f_sold = q_cur_stage['ticketsSold']
  f_avaib = q_cur_stage["ticketsAvailable"]

  f_body = f'{hide_link(q_img[0])}'\
    f'💰 {f_data["title"]} 💰\n\n'\
    f'{f_data["description"]}\n'\
    f'💳 Tickets: {f_sold} / {f_sold+f_avaib} 💳\n'\
    f'💎 Price for ticket: {Web3.from_wei(int(q_cur_stage["ticketPrice"]),"ether")}'\
    f' MATIC 💎\n\n'\
    f'Run for: {q_date.strftime("%m/%d/%Y, %H:%M:%S")}\n\n'
  return f_body

@raf_rout.callback_query(Text(text=k_raffles))
@raf_rout.callback_query(Text(text=k_next))
@raf_rout.callback_query(Text(text=k_prev))
@raf_rout.callback_query(Text(startswith = k_category_chose))
async def mt_show_promo(callback: CallbackQuery,state: FSMContext,bot: Bot):
  f_res = get_res(callback)

  f_data = await state.get_data()
  if callback.data.startswith(k_category_chose):
    f_category = callback.data.removeprefix(k_category_chose)
    f_category = s_category_list.index(f_category)

    f_data[k_category] = f_category
  else:
    if k_category in f_data:
      f_category = f_data[k_category]
    else:
      f_category = 0

  if f_category == 0:
    f_rafles_data = await graph_help.get_grahp()
  else:
    f_rafles_data = await graph_help.get_grahp_by_c(f_category)

  if k_page in f_data:
    f_page = f_data[k_page]
  else:
    f_page = 0
  if callback.data == k_next:
    f_page += 1
  elif callback.data == k_prev:
    f_page -= 1

  f_reffls = f_rafles_data['raffles']
  f_msg_list = []
  f_row = 0
  f_start = config.page_size * f_page
  f_end = (config.page_size) * (f_page+1)
  for i in range(f_start, f_end):
    if i >= len(f_reffls):
      break
    q_raf = f_reffls[i]
    q_bt_b = InlineKeyboardBuilder()
    q_bt_b.add(InlineKeyboardButton(text=f_res.reff_join_btn,
                                    callback_data=k_join_ref+q_raf['id']))
    q_body = mt_get_raffle_body(q_raf)
    q_msg = await callback.message.answer(text = q_body,
                reply_markup=q_bt_b.as_markup(resize_keyboard = True),
                parse_mode="HTML")
    f_msg_list.append(q_msg.message_id)
    f_row += 1

  kb_build = InlineKeyboardBuilder()

  if f_page>0:
    kb_build.add(InlineKeyboardButton(text='<<',
                                      callback_data=k_prev))
  if len(f_reffls) > config.page_size * (f_page+1):
    kb_build.add(InlineKeyboardButton(text='>>',
                                    callback_data=k_next))
  if k_category in f_data:
    kb_build.row(InlineKeyboardButton(text=f_res.back,
                                    callback_data=k_category))
  else:
    kb_build.row(get_cancel_btn(f_res))
  f_body = f'{f_res.page} {f_page}'
  if len(f_reffls) == 0:
    f_body = f_res.empty_category
  f_msg = await callback.message.answer(f_body,reply_markup=kb_build.as_markup(resize_keyboard = True))
  f_msg_list.append(f_msg.message_id)
  f_data[k_page] = f_page
  f_data[k_msg_list] = f_msg_list
  await state.set_state(Form.idle)
  await state.set_data(f_data)

  await callback.answer()



@raf_rout.callback_query(Text(startswith=k_category))
async def mt_show_promo(callback: CallbackQuery,state: FSMContext,bot: Bot):
  f_res = get_res(callback)
  f_data = await state.get_data()

  f_bt_b = InlineKeyboardBuilder()
  for q_c in s_category_list:
    f_bt_b.add(InlineKeyboardButton(text=q_c,
                                  callback_data=k_category_chose + q_c))
  f_bt_b.adjust(4)
  f_bt_b.row(get_cancel_btn(f_res))
  await callback.message.answer(f"{f_res.category}:",reply_markup=f_bt_b.as_markup(resize_keyboard = True))
  await callback.answer()


@raf_rout.callback_query(Text(startswith=k_join_ref))
async def mt_show_promo(callback: CallbackQuery,state: FSMContext):
  f_res = get_res(callback)
  if not await mt_check_adress(callback):
    return
  f_data = callback.data.removeprefix(k_join_ref)
  f_json = await state.get_data()
  q_raf = await graph_help.get_graph_by_id(f_data)
  q_raf = q_raf['raffle']
  f_json[k_chose_ticket] = q_raf
  await state.set_state(Form.input_ticket)

  q_cur_stage = 0
  q_stages = q_raf['stages']
  if len(q_stages) > 1:
      q_cur_stage = next(x for x in q_stages if x['stageType'] == q_raf['ongoingStage'])
  else:
      q_cur_stage = q_stages[0]
  f_body = mt_get_raffle_body(q_raf)
  f_msg_list = []
  f_msg = await callback.message.answer(f_body,parse_mode="HTML")
  f_msg_list.append(f_msg)
  f_data = f_data.removeprefix('0x')
  kb_build = InlineKeyboardBuilder()
  f_url = f"https://raffle.markets/raffle/{f_data}"

  kb_build.add(InlineKeyboardButton(text= '1💳',
                                    callback_data=k_chose_ticket+'1'))
  kb_build.add(InlineKeyboardButton(text=f'max( {q_cur_stage["ticketsAvailable"]}💳 ) ',
                                    callback_data=k_chose_ticket+q_cur_stage["ticketsAvailable"]))
  kb_build.row(InlineKeyboardButton(text='Raffle.markets',
                                    url=f_url))
  kb_build.row(InlineKeyboardButton(text=f_res.back,
                                      callback_data=k_raffles))
  await callback.answer()
  f_body2 = f_res.chose_ticket
  # f_body = f'{f_res.go_to_rafle} {f_url}'
  f_msg = await callback.message.answer(f_body2,
                                reply_markup=kb_build.as_markup(resize_keyboard = True))
  f_msg_list.append(f_msg)
  # f_json[k_msg_list] = f_msg_list
  await state.set_data(f_json)

@raf_rout.callback_query(Text(startswith=k_chose_ticket))
@raf_rout.message(Form.input_ticket)
async def mt_show_promo(callback: CallbackQuery,state: FSMContext):
  f_res = get_res(callback)
  if not await mt_check_adress(callback):
    return

  if isinstance(callback,CallbackQuery):
    f_count_ticket = callback.data.removeprefix(k_chose_ticket)
    await callback.answer()
    await mt_chose_ticket2(f_res,callback.message,f_count_ticket,state)
  else:
    message: Message = callback
    f_count_ticket = message.text
    if not (f_count_ticket).isdigit():
      await message.answer('Введите норм число')
      return
    await mt_chose_ticket2(f_res,message,f_count_ticket,state)

def mt_get_link(f_id):
  f_data = f_id.removeprefix('0x')
  f_url = f"https://raffle.markets/raffle/{f_data}"
  return f_url

async def mt_join_to_rafle_msg(f_data,bot: Bot,message):
  f_res = get_res(message)
  f_url = mt_get_link(f_data['id'])
  f_body = f'{f_res.go_to_rafle}'
  kb_build = InlineKeyboardBuilder()
  kb_build.row(InlineKeyboardButton(text='Raffle.markets',
                                    url=f_url))
  kb_build.row(InlineKeyboardButton(text=f_res.back,
                                    callback_data=k_raffles))
  await bot.send_message(message.from_user.id,f_body,reply_markup=kb_build.as_markup(resize_keyboard = True))

async def mt_chose_ticket2(f_res,message: Message,f_count_ticket,state: FSMContext):
  kb_build = InlineKeyboardBuilder()
  kb_build.row(InlineKeyboardButton(text=f_res.back,
                                    callback_data=k_raffles))

  f_count_ticket = int(f_count_ticket)
  f_json = await state.get_data()
  f_json = f_json[k_chose_ticket]
  q_stages = f_json['stages']
  if len(q_stages) > 1:
    q_cur_stage = next(x for x in q_stages if x['stageType'] == f_json['ongoingStage'])
  else:
    q_cur_stage = q_stages[0]

  f_tic_avaible = int(q_cur_stage['ticketsAvailable'])
  if f_tic_avaible< f_count_ticket:
    await message.answer('Столько билетов нет',reply_markup=kb_build.as_markup(resize_keyboard = True))
    return

  f_price = Web3.from_wei(int(q_cur_stage["ticketPrice"]),"ether")
  f_total_amount = f_price * f_count_ticket

  kb_build = InlineKeyboardBuilder()
  kb_build.row(InlineKeyboardButton(text=f_res.deposit_for_btn + f'{f_total_amount} MATIC',
                                    callback_data=k_deposit_for+str(f_total_amount)))
  kb_build.row(InlineKeyboardButton(text=f_res.back,
                                    callback_data=k_raffles))

  await message.answer(f'{f_res.for_ticket_deposit} {f_total_amount} MATIC\n'
                       f'{f_res.you_can_get_matic}',reply_markup=kb_build.as_markup(resize_keyboard = True))
