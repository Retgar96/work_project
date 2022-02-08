import asyncio
from asyncio import exceptions, log
import Currency
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token="1775416764:AAE05rKKLfYuKdRKuh4ytffGMGsHED0Hsko")
dp = Dispatcher(bot)
cur = Currency.Currency()
user_id = 0

async def on_startup(_):
    print('Бот вышел онлайн')

@dp.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    print(user_id)
    await send_message(user_id, 'test')

async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text == 'Привет':
        await message.answer('Курс битка сейчас:', cur.get_currency_price(), 'доляров')
    # await message.answer('Курс битка сейчас: ', cur.get_currency_price())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True
                           , on_startup=on_startup
                           )
    send_message(user_id, "test")
