# This is a sample Python script.
import asyncio

from referal_bot.routs import main_ref_bot
from referal_bot.target_bot.routs import main_targ_bot


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


async def init_async_stuff():
    asyncio.create_task(main_ref_bot.main())
    await main_targ_bot.main()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    asyncio.get_event_loop()\
        .run_until_complete(
        asyncio.get_event_loop().create_task(init_async_stuff()))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
