from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from teleAgent.api import api_router
from teleAgent.core.config import settings
from teleAgent.core.di import setup_injector
from teleAgent.integrations.telegram import TelegramBot


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    try:
        # Initialize DI container
        injector = setup_injector()
        app.state.injector = injector

        # Get telegram bot instance from DI
        bot = injector.get(TelegramBot)

        # Initialize and start the bot
        await bot.initialize()
        await bot.application.initialize()
        await bot.application.start()
        await bot.application.updater.start_polling()
        logging.info(f"Telegram bot started successfully")

        yield

    finally:
        # Shutdown the bot
        if hasattr(app.state, "injector"):
            bot = app.state.injector.get(TelegramBot)
            if bot.application:
                await bot.application.updater.stop()
                await bot.application.stop()
                await bot.application.shutdown()
                logging.info(f"Telegram bot stopped successfully")

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan
    )

    # Register routes
    app.include_router(api_router)

    return app

app = create_app()