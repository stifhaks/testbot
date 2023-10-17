from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender


# Это будет inner-мидлварь на сообщения
class Lvl2MidlwareMsg(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        result =  await handler(event, data)



        return result



# Это будет outer-мидлварь на любые колбэки
class Lvl2MidlwareClb(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        await event.answer(
            "Бот по выходным не работает!",
            show_alert=True
        )
        return