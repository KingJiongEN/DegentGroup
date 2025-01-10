from typing import Dict
from injector import Module, provider, singleton

from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService
from teleAgent.core.config import settings

from .telegram import TelegramBot

from injector import Module, multiprovider, singleton
from typing import Dict

from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService
from teleAgent.core.config import settings
from teleAgent.integrations.telegram import TelegramBot

class IntegrationsModule(Module):
    @singleton
    @multiprovider
    def provide_telegram_bots(
        self,
        agentService: IAgentService,
        walletService: IWalletService,
        nftService: INFTService,
    ) -> TelegramBot:
        # Retrieve the bot configuration from environment variables
        bot_id = settings.TELEGRAM_BOT_ID
        bot_token = settings.TELEGRAM_TOKEN
        bot_username = settings.TELEGRAM_USERNAME

        # Construct the agent_config dictionary
        agent_config = {
            'id': bot_id,
            'telegram_token': bot_token,
            'username': bot_username
        }

        # Create the TelegramBot instance with the constructed agent_config
        bot = TelegramBot(
            agent_service=agentService,
            wallet_service=walletService,
            nft_service=nftService,
            bot_config=agent_config
        )

        return bot
