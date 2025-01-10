# Basic Bot Setup Tutorial

This tutorial will guide you through creating a basic TeleAgent bot with essential features.

## Overview

We'll create a bot that can:
1. Respond to basic commands
2. Handle different types of messages
3. Manage group conversations
4. Implement basic memory and state management

## Project Structure

```
my_bot/
├── config/
│   └── config.py
├── handlers/
│   ├── __init__.py
│   ├── commands.py
│   ├── messages.py
│   └── media.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── .env
├── requirements.txt
└── main.py
```

## Step 1: Project Setup

1. **Create Project Directory**
   ```bash
   mkdir my_bot
   cd my_bot
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install teleAgent python-dotenv logging
   ```

3. **Create Requirements File**
   ```bash
   pip freeze > requirements.txt
   ```

## Step 2: Configuration

1. **Create `.env` File**
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   OPENAI_API_KEY=your_openai_key
   ```

2. **Create Configuration Module**
   ```python
   # config/config.py
   import os
   from dotenv import load_dotenv

   load_dotenv()

   class Config:
       TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
       TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
       TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
       OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

       # Bot Configuration
       COMMAND_PREFIX = "/"
       MAX_MESSAGE_LENGTH = 4096
       RATE_LIMIT = 5  # messages per second
   ```

## Step 3: Command Handlers

```python
# handlers/commands.py
from teleAgent.integrations.telegram import TelegramClient
from teleAgent.models.agent_model.user_groupagent import UserGroupAgent

class CommandHandlers:
    def __init__(self, client: TelegramClient, agent: UserGroupAgent):
        self.client = client
        self.agent = agent
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on_command("start")
        async def start_command(message):
            welcome_text = (
                "👋 Hello! I'm your TeleAgent bot.\n"
                "Here are some commands you can use:\n"
                "/help - Show available commands\n"
                "/status - Check bot status\n"
                "/settings - Configure bot settings"
            )
            await self.client.send_message(
                chat_id=message.chat.id,
                text=welcome_text
            )

        @self.client.on_command("help")
        async def help_command(message):
            help_text = await self.agent.generate_help_text()
            await self.client.send_message(
                chat_id=message.chat.id,
                text=help_text
            )

        @self.client.on_command("status")
        async def status_command(message):
            status = await self.agent.get_status()
            await self.client.send_message(
                chat_id=message.chat.id,
                text=f"Bot Status:\n{status}"
            )
```

## Step 4: Message Handlers

```python
# handlers/messages.py
from teleAgent.utilities.rate_limiter import RateLimiter

class MessageHandlers:
    def __init__(self, client: TelegramClient, agent: UserGroupAgent):
        self.client = client
        self.agent = agent
        self.rate_limiter = RateLimiter(max_requests=5, time_window=60)
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on_message()
        @self.rate_limiter.limit
        async def handle_message(message):
            # Process message with agent
            response = await self.agent.process_message(message)
            
            # Send response
            if response:
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=response
                )

        @self.client.on_edited_message()
        async def handle_edited_message(message):
            await self.agent.process_edited_message(message)
```

## Step 5: Media Handlers

```python
# handlers/media.py
class MediaHandlers:
    def __init__(self, client: TelegramClient, agent: UserGroupAgent):
        self.client = client
        self.agent = agent
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on_photo()
        async def handle_photo(message):
            photo = await message.photo[-1].download()
            caption = await self.agent.analyze_photo(photo)
            await self.client.send_message(
                chat_id=message.chat.id,
                text=f"Photo analysis: {caption}"
            )

        @self.client.on_document()
        async def handle_document(message):
            doc_info = await self.agent.process_document(message.document)
            await self.client.send_message(
                chat_id=message.chat.id,
                text=f"Document info: {doc_info}"
            )
```

## Step 6: Main Application

```python
# main.py
import asyncio
import logging
from config.config import Config
from teleAgent.integrations.telegram import TelegramClient
from teleAgent.models.agent_model.user_groupagent import UserGroupAgent
from handlers.commands import CommandHandlers
from handlers.messages import MessageHandlers
from handlers.media import MediaHandlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize client
        client = TelegramClient({
            "bot_token": Config.TELEGRAM_BOT_TOKEN,
            "api_id": Config.TELEGRAM_API_ID,
            "api_hash": Config.TELEGRAM_API_HASH
        })

        # Initialize agent
        agent = UserGroupAgent(
            name="BasicBot",
            system_message="I am a helpful group chat assistant",
            llm_config={"model": "gpt-4"}
        )

        # Setup handlers
        CommandHandlers(client, agent)
        MessageHandlers(client, agent)
        MediaHandlers(client, agent)

        # Start the bot
        logger.info("Starting bot...")
        await client.start()
        await client.run_forever()

    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 7: Running the Bot

1. **Verify Configuration**
   - Check all environment variables are set
   - Verify bot token with BotFather
   - Test API keys

2. **Start the Bot**
   ```bash
   python main.py
   ```

## Best Practices

1. **Error Handling**
   ```python
   try:
       await operation()
   except TelegramError as e:
       logger.error(f"Telegram error: {e}")
       # Implement retry logic or fallback
   except Exception as e:
       logger.error(f"Unexpected error: {e}")
       # Notify admin or take appropriate action
   ```

2. **Memory Management**
   ```python
   # Implement cleanup routines
   async def cleanup_old_messages():
       while True:
           await agent.cleanup_memory()
           await asyncio.sleep(3600)  # Run every hour
   ```

3. **Performance Optimization**
   ```python
   # Cache frequently used data
   from functools import lru_cache

   @lru_cache(maxsize=100)
   async def get_user_preferences(user_id: int):
       return await database.fetch_user_preferences(user_id)
   ```

## Testing

```python
# test_bot.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_start_command():
    message = AsyncMock()
    message.chat.id = 123456789
    
    with patch('teleAgent.integrations.telegram.TelegramClient') as mock_client:
        client = mock_client.return_value
        await start_command(message)
        
        client.send_message.assert_called_once_with(
            chat_id=123456789,
            text="👋 Hello! I'm your TeleAgent bot."
        )
```

## Next Steps

1. Add more advanced features:
   - Custom keyboards
   - Inline queries
   - Callback queries

2. Implement additional functionality:
   - User preferences
   - Admin commands
   - Analytics tracking

3. Explore other tutorials:
   - [NFT Creation](nft-creation.md)
   - [Group Chat Integration](group-chat.md)
   - [Bargaining System](bargaining-system.md) 