import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties


from config import BOT_TOKEN
from handlers.admin_msg_handler import admin_message_router
from handlers.commands_handlers import commands_router
from handlers.client_ads_handlers import ads_router

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode='HTML',
            link_preview_is_disabled=True
        )
    )
    dp = Dispatcher()
    dp.include_routers(
        commands_router, admin_message_router,ads_router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")