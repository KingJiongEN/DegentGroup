# Telegram API Reference

Comprehensive documentation for the TeleAgent Telegram integration module.

## TelegramClient

The main class for interacting with Telegram's Bot API.

### Constructor

```python
def __init__(self, config: dict):
    """
    Initialize TelegramClient.
    
    Args:
        config (dict): Configuration dictionary containing:
            - bot_token (str): Telegram bot token
            - api_id (str): Telegram API ID
            - api_hash (str): Telegram API hash
            
    Raises:
        ValueError: If required config values are missing
        TelegramError: If initialization fails
    """
```

### Methods

#### Message Handling

```python
async def on_message(self):
    """
    Decorator for handling new messages.
    
    Example:
        @client.on_message()
        async def handle_message(message):
            await message.reply("Received your message!")
    """

async def on_edited_message(self):
    """
    Decorator for handling edited messages.
    
    Example:
        @client.on_edited_message()
        async def handle_edit(message):
            await message.reply("Message was edited!")
    """

async def on_command(self, command: str):
    """
    Decorator for handling bot commands.
    
    Args:
        command (str): Command name without '/'
        
    Example:
        @client.on_command("start")
        async def handle_start(message):
            await message.reply("Bot started!")
    """
```

#### Message Sending

```python
async def send_message(
    self,
    chat_id: Union[int, str],
    text: str,
    parse_mode: str = None,
    reply_markup: dict = None
) -> dict:
    """
    Send text message to a chat.
    
    Args:
        chat_id: Unique identifier for the target chat
        text: Message text
        parse_mode: Text parsing mode (HTML/Markdown)
        reply_markup: Additional interface options
        
    Returns:
        dict: Sent message information
        
    Raises:
        TelegramError: If message sending fails
    """

async def send_photo(
    self,
    chat_id: Union[int, str],
    photo: Union[str, bytes],
    caption: str = None,
    reply_markup: dict = None
) -> dict:
    """
    Send photo to a chat.
    
    Args:
        chat_id: Unique identifier for the target chat
        photo: Photo to send (file_id, URL, or bytes)
        caption: Photo caption
        reply_markup: Additional interface options
        
    Returns:
        dict: Sent message information
        
    Raises:
        TelegramError: If photo sending fails
    """
```

#### Group Management

```python
async def get_chat_member(
    self,
    chat_id: Union[int, str],
    user_id: int
) -> dict:
    """
    Get information about a chat member.
    
    Args:
        chat_id: Unique identifier for the target chat
        user_id: Unique identifier of the target user
        
    Returns:
        dict: Chat member information
        
    Raises:
        TelegramError: If request fails
    """

async def ban_chat_member(
    self,
    chat_id: Union[int, str],
    user_id: int,
    until_date: int = None
) -> bool:
    """
    Ban a user in a group.
    
    Args:
        chat_id: Unique identifier for the target chat
        user_id: Unique identifier of the user to ban
        until_date: Ban duration in Unix time
        
    Returns:
        bool: True on success
        
    Raises:
        TelegramError: If ban fails
    """
```

### Events

```python
async def on_new_chat_members(self):
    """
    Decorator for handling new chat members.
    
    Example:
        @client.on_new_chat_members()
        async def welcome(message):
            for user in message.new_chat_members:
                await message.reply(f"Welcome {user.first_name}!")
    """

async def on_left_chat_member(self):
    """
    Decorator for handling members leaving chat.
    
    Example:
        @client.on_left_chat_member()
        async def goodbye(message):
            user = message.left_chat_member
            await message.reply(f"Goodbye {user.first_name}!")
    """
```

### Error Handling

```python
class TelegramError(Exception):
    """Base exception for Telegram-related errors"""
    pass

class APIError(TelegramError):
    """Exception for API request failures"""
    pass

class AuthError(TelegramError):
    """Exception for authentication failures"""
    pass

class NetworkError(TelegramError):
    """Exception for network-related failures"""
    pass
```

### Types

#### Message

```python
class Message:
    """Represents a Telegram message"""
    
    @property
    def message_id(self) -> int:
        """Unique message identifier"""
        
    @property
    def from_user(self) -> User:
        """Sender of the message"""
        
    @property
    def chat(self) -> Chat:
        """Chat the message belongs to"""
        
    @property
    def text(self) -> Optional[str]:
        """Message text"""
        
    @property
    def photo(self) -> Optional[List[PhotoSize]]:
        """Available photo sizes"""
```

#### User

```python
class User:
    """Represents a Telegram user"""
    
    @property
    def id(self) -> int:
        """Unique identifier for this user"""
        
    @property
    def first_name(self) -> str:
        """User's first name"""
        
    @property
    def last_name(self) -> Optional[str]:
        """User's last name"""
        
    @property
    def username(self) -> Optional[str]:
        """User's username"""
```

### Usage Examples

#### Basic Bot Setup

```python
from teleAgent.integrations.telegram import TelegramClient

async def main():
    # Initialize client
    client = TelegramClient({
        "bot_token": "YOUR_BOT_TOKEN",
        "api_id": "YOUR_API_ID",
        "api_hash": "YOUR_API_HASH"
    })
    
    # Register message handler
    @client.on_message()
    async def echo(message):
        await client.send_message(
            chat_id=message.chat.id,
            text=message.text
        )
    
    # Start the bot
    await client.start()
    await client.run_forever()
```

#### Command Handling

```python
# Register command handler
@client.on_command("start")
async def start_command(message):
    await client.send_message(
        chat_id=message.chat.id,
        text="Welcome to the bot!",
        reply_markup={
            "inline_keyboard": [
                [{
                    "text": "Help",
                    "callback_data": "help"
                }]
            ]
        }
    )
```

#### Error Handling

```python
try:
    await client.send_message(chat_id, text)
except APIError as e:
    logger.error(f"API Error: {e}")
    # Implement retry logic
except NetworkError as e:
    logger.error(f"Network Error: {e}")
    # Wait and retry
except TelegramError as e:
    logger.error(f"Telegram Error: {e}")
    # Handle other errors
``` 