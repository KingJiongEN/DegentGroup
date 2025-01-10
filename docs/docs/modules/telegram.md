# Telegram Integration

The Telegram integration module provides the core functionality for interacting with the Telegram Bot API.

## Overview

```python
from teleAgent.integrations.telegram import TelegramClient
```

The `TelegramClient` class handles all Telegram-related operations, including:
- Message processing
- User management
- Group chat interactions
- Media handling

## Configuration

```python
telegram_config = {
    "bot_token": "YOUR_BOT_TOKEN",
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH"
}

client = TelegramClient(telegram_config)
```

## Key Components

### Message Handler

```python
@client.on_message()
async def handle_message(message):
    """
    Process incoming Telegram messages
    """
    # Message processing logic
    pass
```

### Group Chat Management

```python
async def manage_group_chat(chat_id: int):
    """
    Handle group chat operations
    """
    # Group management logic
    pass
```

## Usage Examples

### Basic Bot Setup

```python
from teleAgent.integrations.telegram import TelegramClient

async def main():
    client = TelegramClient(config)
    await client.start()
    
    @client.on_message()
    async def echo(message):
        await message.reply(message.text)
        
    await client.run()
```

### Advanced Features

- Message filtering
- Media handling
- Inline keyboards
- Callback queries

## Error Handling

```python
try:
    await client.send_message(chat_id, text)
except TelegramError as e:
    logger.error(f"Failed to send message: {e}")
```

## Best Practices

1. Always handle exceptions
2. Use rate limiting
3. Implement proper logging
4. Follow Telegram Bot API guidelines 