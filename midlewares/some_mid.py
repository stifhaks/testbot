from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender


# Это будет inner-мидлварь на сообщения
class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        f_id = str(event.from_user.id)
        f_clb = data['handler'].filters[0].callback
        print(f'{event.date}: {f_id}: {str(f_clb)}')

        ChatActionSender(
            action="upload_video_note",
            chat_id=event.chat.id
        )
        result =  await handler(event, data)

        return result


k_msg_list = 'msg_list'

# Это будет outer-мидлварь на любые колбэки
class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        f_id = str(event.from_user.id)
        if len(data['handler'].filters)>0:
            f_clb = data['handler'].filters[0].callback
        else:
            f_clb = 'NO FILTERS'
        f_data = await data['state'].get_data()
        if k_msg_list in f_data:
            f_msgl = f_data[k_msg_list]
            for q_msg in f_msgl:
                await data['bot'].delete_message(event.from_user.id,
                                         q_msg)
            f_data.pop(k_msg_list)
            await data['state'].set_data(f_data)
        print(f'{event.message.date}: {f_id}: {str(f_clb)}')
        return await handler(event, data)
