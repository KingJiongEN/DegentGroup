# Telegram Bot Tutorial

This tutorial explains the key components of the TeleAgent Telegram bot implementation.

## Core Features

### 1. Response Handling

The bot uses a flexible `TelegramResponse` class to handle different types of responses:

```python
@dataclass
class TelegramResponse:
    text: Optional[str] = None
    image: Optional[Union[str, bytes, BinaryIO]] = None
    caption: Optional[str] = None
    video: Optional[Union[str, bytes, BinaryIO]] = None
    audio: Optional[Union[str, bytes, BinaryIO]] = None
    document: Optional[Union[str, bytes, BinaryIO]] = None
```

This allows sending:
- Text-only messages
- Images with captions
- Combined text and media messages
- Various media types (images, videos, audio, documents)

### 2. Available Commands

The bot supports these main commands:

```python
/start      - Start interaction with the bot
/help       - Show available commands
/profile    - View agent profile & style
/mint       - Check latest minted NFTs
/nfts       - View agent's NFT collection
/balance    - Check token balance
```

### 3. Message Handling

Messages are processed through the `handle_message` method which:
- Receives updates from Telegram
- Processes messages through the agent service
- Handles both private and group chat messages
- Supports response delays for group chats

Example usage:
```python
@bot.message_handler(func=lambda message: True)
async def handle_message(update: Update, context):
    response = await agent_service.get_response(
        bot_id=context.bot.id,
        update=update,
        message=update.message.text
    )
    await message_reply(chat_id, response)
```

### 4. Group Chat Support

The bot includes special handling for group chats:
- Maintains group chat intervals
- Processes bot responses in groups
- Supports multi-bot interactions
- Implements rate limiting

### 5. Redis Integration

For message queueing and persistence:
```python
# Push message to queue
/push_redis <message>

# Pop message from queue
/pop_redis
```

## Basic Setup

1. Initialize the bot with required services:
```python
bot = TelegramBot(
    agent_service=agent_service,
    wallet_service=wallet_service,
    nft_service=nft_service,
    bot_config=config
)
```

2. Set up command handlers:
```python
self.application.add_handler(CommandHandler("start", self.start))
self.application.add_handler(CommandHandler("help", self.help))
# ... additional handlers
```

3. Start the bot:
```python
await bot.initialize()
```

## Important Notes

- Ensure privacy mode is disabled via @BotFather
- Configure proper error handling
- Set up appropriate rate limiting for group chats
- Handle media responses appropriately
- Maintain proper service dependencies

For more details, refer to the implementation in `telegram.py`. 