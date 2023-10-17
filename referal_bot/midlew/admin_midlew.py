from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

import config


class AdminMessageMidleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
      f_id = event.from_user.id
      if f_id in config.s_admins:
        result = await handler(event, data)
        return result


        # if f_id in config.s_admins:
        # 	result = await handler(event, data)
        #
        # 	return result
        #
        # return 0
