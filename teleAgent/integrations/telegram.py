import base64
import logging
from typing import Dict, List, Optional
import asyncio
import random
from dataclasses import dataclass
from typing import Optional, Union, BinaryIO
import json
from datetime import datetime

from telegram import Update, Message, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.error import TelegramError
from redis import Redis

from teleAgent.core.config import settings
from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService
from teleAgent.constants import DRAWING_PROBABILITY, GROUP_CHAT_INTERVAL, ARTWORK_CREATION_INTERVAL, MARKET_ADJUSTMENT_PROBABILITY

from teleAgent.plugins.plugin_solana.tools.check_balance import check_wallet_balance_return_str
from teleAgent.plugins.plugin_solana.tools.create_nft import create_nft_with_generation
from teleAgent.plugins.plugin_solana.tools.transfer_nft import transfer_nft
from teleAgent.plugins.plugin_solana.tools.transfer_token import transfer_token

@dataclass
class TelegramResponse:
    """Class to handle different types of Telegram responses"""
    text: Optional[str] = None
    image: Optional[Union[str, bytes, BinaryIO]] = None
    caption: Optional[str] = None
    video: Optional[Union[str, bytes, BinaryIO]] = None
    audio: Optional[Union[str, bytes, BinaryIO]] = None
    document: Optional[Union[str, bytes, BinaryIO]] = None
    
    @classmethod
    def text_response(cls, text: str) -> 'TelegramResponse':
        """Create a text-only response"""
        return cls(text=text)
    
    @classmethod
    def image_response(cls, image: Union[str, bytes, BinaryIO], caption: Optional[str] = None) -> 'TelegramResponse':
        """Create an image response with optional caption"""
        return cls(image=image, caption=caption)
    
    @classmethod
    def media_with_text(cls, text: str, **kwargs) -> 'TelegramResponse':
        """Create a response with both text and media"""
        return cls(text=text, **kwargs)

    def has_media(self) -> bool:
        """Check if response contains any media"""
        return any([self.image, self.video, self.audio, self.document])


class TelegramBot:
    def __init__(
        self,
        agent_service: IAgentService,
        wallet_service: IWalletService,
        nft_service: INFTService,
        bot_config: Dict[str, str]
    ):
        self.application = None
        self.agent_service = agent_service
        self.nft_service = nft_service
        self.wallet_service = wallet_service
        self.bot_config = bot_config
        self.group_chat_id = None
        self.redis_client = Redis(host='redis', port=6379, db=0)
        
    async def initialize(self):
        """Initialize bot application"""
        if not self.application:
            self.application = (
                Application.builder()
                .token(self.bot_config['telegram_token'])
                .build()
            )
            
            await self._verify_privacy_settings()
            self._setup_handlers()
            logging.info(f"Telegram bot {self.bot_config['id']} initialized")

    async def _verify_privacy_settings(self):
        """Verify and log privacy mode settings"""
        try:
            bot_info = await self.application.bot.get_me()
            logging.info(f"Bot {bot_info.username} initialized. Please ensure privacy mode is disabled via @BotFather")
            logging.info("Use the following commands with @BotFather:")
            logging.info("1. /mybots")
            logging.info(f"2. Select @{bot_info.username}")
            logging.info("3. Select 'Bot Settings'")
            logging.info("4. Select 'Group Privacy'")
            logging.info("5. Select 'Turn off'")
            
        except Exception as e:
            logging.error(f"Failed to verify bot privacy settings: {str(e)}")
            raise

    def _setup_handlers(self):
        """Setup message handlers"""
        if not self.application:
            return

        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("profile", self.profile))
        self.application.add_handler(CommandHandler("mint", self.mint))
        self.application.add_handler(CommandHandler("nfts", self.nfts))
        self.application.add_handler(CommandHandler("balance", self.balance))

        self.application.add_handler(CommandHandler("clean_history", self.clean_history))

        if settings.TELEGRAM_TOOLS_TEST:
            self.application.add_handler(CommandHandler("test_check_balance", self.test_check_balance))
            self.application.add_handler(CommandHandler("test_create_nft", self.test_create_nft))
            self.application.add_handler(CommandHandler("test_transfer_nft", self.test_transfer_nft))
            self.application.add_handler(CommandHandler("test_transfer_token", self.test_transfer_token))
            self.application.add_handler(CommandHandler("push_redis", self.push_redis))
            self.application.add_handler(CommandHandler("pop_redis", self.pop_redis))
            self.application.add_handler(CommandHandler("draw_test", self.draw))
            self.application.add_handler(CommandHandler("market_adjust", self.market_adjust))
            self.application.add_handler(CommandHandler("message_test", self.message_test))
            
        # Message handler - Handle both private and group messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )


    def _get_commands_help(self, include_test: bool = False) -> str:
        """Generate command help text"""
        commands = {
            "start": "Start interaction",
            "help": "Show this help message",
            "profile": "View agent profile & style",
            "mint": "Check latest minted NFTs",
            "nfts": "View agent's NFT collection",
            "balance": "Check token balance",
            "clean_history": "Clean chat history with the bot",
            "draw_test": "Draw a test artwork",
            "market_adjust": "Adjust market",
            "push_redis": "Push a message to Redis queue",
            "pop_redis": "Pop a message from Redis queue"
        }
        
        test_commands = {
            "test_check_balance": {
                "desc": "Check wallet balance",
                "usage": None
            },
            "test_create_nft": {
                "desc": "Create test NFT",
                "usage": "<prompt> - Text prompt for NFT generation"
            },
            "test_transfer_nft": {
                "desc": "Transfer NFT to another wallet",
                "usage": "<token_id> <to_address> - NFT ID and recipient address"
            },
            "test_transfer_token": {
                "desc": "Transfer tokens to another wallet",
                "usage": "<to_address> <amount> [token_mint] - Recipient, amount and optional token mint"
            }
        }

        help_text = "Available commands:\n"
        for cmd, desc in commands.items():
            help_text += f"/{cmd} - {desc}\n"

        if include_test and settings.TELEGRAM_TOOLS_TEST:
            help_text += "\nTest Commands:\n"
            for cmd, info in test_commands.items():
                help_text += f"/{cmd} - {info['desc']}\n"
                if info['usage']:
                    help_text += f"    Usage: /{cmd} {info['usage']}\n"

        return help_text

    async def start(self, update: Update, context):
        """Handle /start command"""
        welcome_text = (
            f"Hello {update.effective_user.first_name}! Welcome to TraderAI.\n\n"
            "I'm your AI companion in the crypto art world. Here are my available commands:\n\n"
        )
        help_text = self._get_commands_help(include_test=True)
        await update.message.reply_text(
            welcome_text + help_text + "\nFeel free to chat with me about NFTs, crypto art, or anything creative!"
        )

    async def help(self, update: Update, context):
        """Handle /help command"""
        help_text = self._get_commands_help(include_test=True)
        await update.message.reply_text(
            "TraderAI Command Reference:\n\n" + help_text + "\nYou can also chat with me directly!"
        )

    async def profile(self, update: Update, context):
        """Handle /profile command"""
        bot_id = context.bot.id
        agent = self.agent_service.get_by_id(str(bot_id))
        profile = (
            f"Agent Profile: {agent.name_str}\n"
            f"Personality: {agent.personality}\n"
            f"Art Style: {agent.art_style}\n"
        )
        await update.message.reply_text(profile)

    async def mint(self, update: Update, context):
        """Handle /mint command"""
        latest_nfts = await self.nft_service.get_latest_mints()
        if not latest_nfts:
            await update.message.reply_text("No recent NFTs have been minted.")
            return

        nft_list = "Recently Minted NFTs:\n"
        for nft in latest_nfts:
            nft_list += f"- {nft.name} by {nft.creator}\n"
        await update.message.reply_text(nft_list)

    async def nfts(self, update: Update, context):
        """Handle /nfts command"""
        
        bot_id = context.bot.id
        agent = self.agent_service.get_by_id(str(bot_id))
        nfts = await self.nft_service.get_agent_nfts(agent.id)

        if not nfts:
            await update.message.reply_text(
                "I don't have any NFTs in my collection yet."
            )
            return

        collection = f"My NFT Collection ({len(nfts)} total):\n"
        for nft in nfts:
            collection += f"- {nft.name} ({nft.style})\n"
        await update.message.reply_text(collection)

    async def balance(self, update: Update, context):
        """Handle /balance command"""
        agent = await self.agent_service.get_agent_for_chat(update.effective_chat.id)
        balance = await self.wallet_service.get_balance(agent.wallet_address)
        balance_text = f"Current Balance: {balance.amount} {balance.token_symbol}"
        await update.message.reply_text(balance_text)

    async def draw(self, update: Update, context):
        """Handle /draw command"""
        logging.info(f"Drawing test artwork for agent {self.bot_config['id']}")
        agent = self.agent_service.get_by_id(self.bot_config['id'])
        response_artwork = await self.agent_service.act_periodically_artwork_creation(agent)
        await self.message_reply(update.effective_chat.id, response_artwork)

    async def market_adjust(self, update: Update, context):
        """Handle /market_adjust command"""
        agent = self.agent_service.get_by_id(self.bot_config['id'])
        response_market = await self.agent_service.act_periodically_market_adjust(agent)
        if response_market:
            await update.message.reply_text(str(response_market))
        else:
            await update.message.reply_text("No potential buyers found")
    
    async def message_test(self, update: Update, context):
        """Handle /message_test command"""
        
        img_path = f"teleAgent/templates/DealMadePic.jpg"
        with open(img_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        response = TelegramResponse.media_with_text('deal made test', image=base64_image)
        await self.message_reply(update.effective_chat.id, response)
    
    async def message_reply(self, chat_id: int, response: TelegramResponse) -> Optional[Message]:
        """Send a response to a specific chat"""
        try:
            if not response:
                return None

            sent_message = None
            
            # If there's media with text, send text first then media
            if response.text and response.has_media():
                await self.application.bot.send_message(chat_id=chat_id, text=response.text)
            
            # Handle different types of media
            if response.image:
                sent_message = await self.application.bot.send_photo(
                    chat_id=chat_id,
                    photo=response.image,
                    caption=response.caption
                )
            elif response.video:
                sent_message = await self.application.bot.send_video(
                    chat_id=chat_id,
                    video=response.video,
                    caption=response.caption
                )
            elif response.audio:
                sent_message = await self.application.bot.send_audio(
                    chat_id=chat_id,
                    audio=response.audio,
                    caption=response.caption
                )
            elif response.document:
                sent_message = await self.application.bot.send_document(
                    chat_id=chat_id,
                    document=response.document,
                    caption=response.caption
                )
            # If no media but has text, send text
            elif response.text:
                sent_message = await self.application.bot.send_message(
                    chat_id=chat_id,
                    text=response.text
                )
                
            return sent_message
            
        except Exception as e:
            print(f"Error sending telegram message: {str(e)}")
            # Fallback to simple text message in case of error
            return await self.application.bot.send_message(
                chat_id=chat_id,
                text="Sorry, I encountered an error while processing your request."
            )

    async def handle_message(self, update: Update, context):
        """Handle normal chat messages"""
        logging.info(f"Received message in chat type: {update.effective_chat.type}")
        logging.info(f"Message text: {update.message.text}")

        bot_id = context.bot.id
        
        # Pass the raw message to agent service
        response = await self.agent_service.get_response(
            bot_id=bot_id,
            update=update,
            message=update.message.text,
        )

        if response:
            chat_id = update.effective_chat.id
            sent_message = None
            
            # Handle MultiResponse 
            if hasattr(response, 'to_telegram_responses'):
                telegram_responses = response.to_telegram_responses()
                for resp in telegram_responses:
                    sent_message = await self.message_reply(chat_id, resp)
                    # Add a small delay between messages
                    await asyncio.sleep(0.4)
            else:
                sent_message = await self.message_reply(chat_id, response)
            
            if update.effective_chat.type in ['group', 'supergroup'] and sent_message:
                if self.group_chat_id:
                    assert self.group_chat_id == chat_id, "Currently, we only support one group chat for a bot. "
                else:
                    print(f"Setting group chat id to {chat_id}")
                    self.group_chat_id = chat_id
                
                await asyncio.sleep(GROUP_CHAT_INTERVAL)

                # Create a new Update object for the bot's responses
                new_update = Update.de_json({
                    'update_id': update.update_id + 1,
                    'message': {
                        'message_id': sent_message.message_id,
                        'from': {
                            'id': bot_id,
                            'is_bot': True,
                            'first_name': context.bot.first_name,
                            'username': context.bot.username
                        },
                        'chat': update.effective_chat.to_dict(),
                        'date': int(sent_message.date.timestamp()),
                        'text': response.text if isinstance(response, TelegramResponse) else str(response)
                    }
                }, context.bot)

                # Process the new update asynchronously
                asyncio.create_task(self._process_bot_response(new_update, context))

    async def _process_bot_response(self, update: Update, context):
        """Process responses to bot messages"""
        # Only process if the message is from another bot
        if update.effective_message.from_user.is_bot:
            await self.handle_message(update, context)

    async def stop(self):
        """Stop the bot and cleanup tasks"""
        if self._periodic_task and not self._periodic_task.done():
            self._periodic_task.cancel()
            try:
                await self._periodic_task
            except asyncio.CancelledError:
                pass

    async def test_check_balance(self, update: Update, context):
        """Handle /test_check_balance command"""
        balances_desc = await check_wallet_balance_return_str(settings.METAPLEX_PUBLIC_KEY)
        await update.message.reply_text(balances_desc)

    async def test_create_nft(self, update: Update, context):
        """Handle /test_create_nft command"""
        try:
            # Extract the prompt from the command line arguments
            if len(context.args) == 0:
                await update.message.reply_text("Please provide a prompt for the NFT creation.")
                return
        
            prompt = " ".join(context.args)

            # Define test parameters
            wallet_address = settings.METAPLEX_PUBLIC_KEY  # Replace with a valid test wallet address
            name = "Test NFT"
            creator_id = settings.METAPLEX_PUBLIC_KEY  # Replace with a valid creator ID
            style = None
            metadata = None  # Leave metadata as None as per the requirement

            # Create the NFT using the provided function
            result = await create_nft_with_generation(
                wallet_address=wallet_address,
                name=name,
                prompt=prompt,
                creator_id=creator_id,
                style=style,
                metadata=metadata
            )

            # Send a response back to the user
            if result.success and result.nft:
                response_text = (
                    f"Test NFT created successfully!\n"
                    f"Name: {result.nft.metadata.name}\n"
                    f"Image URL: {result.image_url}\n"
                    f"Metadata URL: {result.metadata_url}"
                )
            else:
                response_text = f"Failed to create test NFT. Error: {result.error}"

            await update.message.reply_text(response_text)

        except Exception as e:
            # Handle any errors that occur during NFT creation
            logging.error(f"Error creating test NFT: {str(e)}")
            await update.message.reply_text("Failed to create test NFT. Please try again later.")

    async def test_transfer_nft(self, update: Update, context):
        """Handle /test_transfer_nft command"""
        try:
            if len(context.args) != 2:
                await update.message.reply_text(
                    "Please provide both token_id and to_address.\n"
                    "Usage: /test_transfer_nft <token_id> <to_address>"
                )
                return

            token_id = context.args[0]
            to_address = context.args[1]

            result = await transfer_nft(
                token_id=token_id,
                to_address=to_address
            )

            if result.success:
                response_text = (
                    f"NFT Transfer Successful!\n"
                    f"Transaction Hash: {result.tx_hash}\n"
                    f"From: {result.from_address}\n"
                    f"To: {result.to_address}\n"
                    f"Token ID: {result.token_id}"
                )
            else:
                response_text = f"Transfer failed. Error: {result.error}"

            await update.message.reply_text(response_text)

        except Exception as e:
            logging.error(f"Error in test_transfer_nft: {str(e)}")
            await update.message.reply_text(
                "Failed to execute NFT transfer. Please try again later."
            )

    async def test_transfer_token(self, update: Update, context):
        """Handle /test_transfer_token command"""
        try:
            if len(context.args) < 2 or len(context.args) > 3:
                await update.message.reply_text(
                    "Usage: /test_transfer_token <to_address> <amount> [token_mint]\n"
                    "Example: /test_transfer_token Ghj45... 1.5 USD4..."
                )
                return

            to_address = context.args[0]
            
            try:
                amount = float(context.args[1])
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError:
                await update.message.reply_text("Amount must be a valid positive number")
                return

            token_mint = context.args[2] if len(context.args) == 3 else None

            result = await transfer_token(
                to_address=to_address,
                amount=amount,
                token_mint=token_mint
            )

            if result.success:
                token_type = "SOL" if not token_mint else f"token {token_mint}"
                response_text = (
                    f"Token Transfer Successful!\n"
                    f"Transaction Hash: {result.tx_hash}\n"
                    f"From: {result.from_address}\n"
                    f"To: {result.to_address}\n"
                    f"Amount: {result.amount} {token_type}\n"
                    f"Fee: {result.fee} SOL"
                )
            else:
                response_text = f"Transfer failed. Error: {result.error}"

            await update.message.reply_text(response_text)

        except Exception as e:
            logging.error(f"Error in test_transfer_token: {str(e)}")
            await update.message.reply_text(
                "Failed to execute token transfer. Please try again later."
            )

    async def clean_history(self, update: Update, context):
        """Handle /clean_history command"""
        try:
            user_id = str(update.effective_user.id)
            bot_id = str(context.bot.id)
            
            # Get dialog records before deletion to count them
            count = self.agent_service.cleanup_user_memory_from_db(agent_id=bot_id, user_id=user_id)
            
            # Clear in-memory messages if any
            if bot_id in self.agent_service._memories and user_id in self.agent_service._memories[bot_id]:
                self.agent_service._memories[bot_id][user_id] = []
            
            response = (
                f"Successfully cleaned chat history!\n"
                f"Deleted {count} messages between you and the bot."
            )
            await update.message.reply_text(response)
            
        except Exception as e:
            logging.error(f"Error cleaning chat history: {str(e)}")
            await update.message.reply_text(
                "Sorry, I encountered an error while cleaning the chat history. "
                "Please try again later."
            )

    async def push_redis(self, update: Update, context):
        """Handle /push_redis command"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "Please provide a message to push.\n"
                    "Usage: /push_redis <message>"
                )
                return

            message = " ".join(context.args)
            
            # Create message data
            message_data = {
                "sender_id": str(update.effective_user.id),
                "sender_name": update.effective_user.first_name,
                "content": message,
                "timestamp": datetime.now().isoformat(),
                "chat_id": update.effective_chat.id
            }

            # Push to Redis list
            self.redis_client.rpush(
                'telegram_bot_messages',
                json.dumps(message_data)
            )

            await update.message.reply_text(
                f"Message pushed to Redis successfully:\n{message}"
            )

        except Exception as e:
            logging.error(f"Error pushing message to Redis: {str(e)}")
            await update.message.reply_text(
                "Failed to push message to Redis. Please try again later."
            )

    async def pop_redis(self, update: Update, context):
        """Handle /pop_redis command"""
        try:
            # Try to get message from Redis list
            message_data = self.redis_client.lpop('telegram_bot_messages')
            
            if not message_data:
                await update.message.reply_text("No messages available in Redis.")
                return

            # Parse message data
            message = json.loads(message_data)
            
            # Format response
            response = (
                f"Message popped from Redis:\n"
                f"From: {message['sender_name']}\n"
                f"Content: {message['content']}\n"
                f"Time: {message['timestamp']}"
            )

            await update.message.reply_text(response)

        except Exception as e:
            logging.error(f"Error popping message from Redis: {str(e)}")
            await update.message.reply_text(
                "Failed to pop message from Redis. Please try again later."
            )

async def validate_bot_configs(bot_configs: List[Dict[str, str]]) -> None:
    """Validate all bot configurations and privacy settings"""
    for config in bot_configs:
        try:
            bot = Bot(token=config['telegram_token'])
            bot_info = await bot.get_me()
            
            logging.info(f"Validating bot: {bot_info.username}")
            logging.info("⚠️ Please verify privacy mode is disabled for this bot via @BotFather")
            
        except TelegramError as e:
            logging.error(f"Failed to validate bot {config['id']}: {str(e)}")
            raise
        finally:
            if bot:
                await bot.close() 

