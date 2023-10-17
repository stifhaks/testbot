from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_keys import user_table, k_addres
from routs.raffle_bot_main import mt_check_adress
from routs.routs_key import k_promo, get_res, get_cancel_btn, db_helper

promo_router = Router()

# {
#   "data": {
#     "raffles": [
#       {
#         "title": "cars",
#         "description": "best car ever",
#         "raffleAddress": "0x8093c66c8f522a5508cea43d1445c3f66e7c2cb7",
#         "raffleEndTime": "300",
#         "raffleTicker": "1",
#         "images": [
#           "https://engvo.me/books/Elementary/book-1.png"
#         ]
#       },

@promo_router.callback_query(Text(text=k_promo))
async def mt_show_promo(callback: CallbackQuery):
  # if not await mt_check_adress(callback):
  #   return
  f_res = get_res(callback)
  kb_build = InlineKeyboardBuilder()
  kb_build.row(get_cancel_btn(f_res))
  f_adress = db_helper.get_cell(user_table,k_addres,callback.from_user.id)
  f_body = f'{f_res.go_to_promo} https://raffle.markets/promo-raffle'

  await callback.message.answer(f_body,reply_markup=kb_build.as_markup(resize_keyboard = True))
  await callback.answer()



