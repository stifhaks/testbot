import asyncio

from aiogram import Router, F, Bot, Dispatcher

import private_key
from referal_bot.routs import main_ref_bot
from routs import promo, raffles, crypto_bot
from routs.raffle_bot_main import form_router

bot = Bot(token=private_key.s_bot_token)
dp = Dispatcher()

from midlewares.some_mid import WeekendMessageMiddleware,WeekendCallbackMiddleware
def getBot():
    return bot


async def main():
    dp.include_router(form_router)
    form_router.include_router(promo.promo_router)
    form_router.include_router(raffles.raf_rout)
    form_router.include_router(crypto_bot.crypto_router)
    asyncio.create_task(main_ref_bot.main())
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