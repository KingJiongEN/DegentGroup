# Getting Started with TeleAgent

This guide will help you set up and run your first TeleAgent instance.

## Prerequisites

Before you begin, ensure you have:

1. Python 3.8 or higher installed
2. A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
3. OpenAI API Key (for GPT-4 and DALL-E)
4. Basic knowledge of Python and async programming

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KingJiongEN/DegentGroup.git
   cd DegentGroup
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Create Environment File**
   ```bash
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   ```env
   # Telegram Configuration
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_key

   # Database Configuration
   DATABASE_URL=sqlite:///./teleagent.db

   # IPFS Configuration (Optional)
   IPFS_NODE_URL=your_ipfs_node
   ```

## Interesting Features 

### 1. Enable NFT Creation

```python
from teleAgent.models.agent_model.artwork_creation import CreativeArtistAgent

# Initialize the artwork creator
artwork_creator = CreativeArtistAgent(
    character_profile="creative and artistic",
    dalle_config={"api_key": "YOUR_OPENAI_KEY"},
    llm_config={"model": "gpt-4"}
)

# Add artwork creation command
@client.on_command("create_nft")
async def create_nft(message):
    # Generate artwork
    artwork = await artwork_creator.create_artwork(message.text)
    
    # Send the artwork
    await client.send_photo(
        chat_id=message.chat.id,
        photo=artwork['url'],
        caption="Here's your generated NFT!"
    )
```

### 2. Enable Bargaining

```python
from teleAgent.models.agent_model.bargain.bargainer import BargainerAgent

# Initialize the bargainer
bargainer = BargainerAgent(
    agent_id="unique_id",
    nft_dao=your_nft_dao
)

# Add bargaining command
@client.on_command("bargain")
async def start_bargaining(message):
    result = await bargainer.start_negotiation(
        context={"message": message}
    )
    await client.send_message(
        chat_id=message.chat.id,
        text=f"Bargaining result: {result}"
    )
```

## Common Operations

### Managing Group Chats

```python
# Enable group management
@client.on_new_chat_members()
async def welcome_new_members(message):
    for user in message.new_chat_members:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"Welcome {user.first_name} to the group!"
        )

# Handle left members
@client.on_left_chat_member()
async def goodbye_member(message):
    user = message.left_chat_member
    await client.send_message(
        chat_id=message.chat.id,
        text=f"Goodbye {user.first_name}!"
    )
```

### Handling Media

```python
# Handle images
@client.on_photo()
async def process_photo(message):
    # Download the photo
    photo = await message.photo[-1].download()
    
    # Process the photo
    result = await process_image(photo)
    
    await client.send_message(
        chat_id=message.chat.id,
        text=f"Processed image result: {result}"
    )
```

## Best Practices

1. **Error Handling**
   ```python
   try:
       result = await some_operation()
   except TelegramError as e:
       logger.error(f"Telegram error: {e}")
       await client.send_message(
           chat_id=message.chat.id,
           text="Sorry, something went wrong!"
       )
   except Exception as e:
       logger.error(f"Unexpected error: {e}")
       await client.send_message(
           chat_id=message.chat.id,
           text="An unexpected error occurred"
       )
   ```

2. **Rate Limiting**
   ```python
   from teleAgent.utilities.rate_limiter import RateLimiter

   rate_limiter = RateLimiter(
       max_requests=5,
       time_window=60  # 1 minute
   )

   @client.on_message()
   @rate_limiter.limit
   async def handle_message(message):
       # Your handler code
       pass
   ```

3. **Logging**
   ```python
   import logging

   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   logger = logging.getLogger(__name__)
   ```

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check if the bot token is correct
   - Ensure the bot has the necessary permissions
   - Verify the internet connection

2. **API Errors**
   - Check API key validity
   - Verify rate limits
   - Check request formatting

3. **Database Issues**
   - Verify database connection string
   - Check database permissions
   - Ensure tables are created properly

### Getting Help

- Check the [GitHub Issues](https://github.com/KingJiongEN/DegentGroup/issues)
- Join our [Telegram Support Group](https://t.me/teleagent_support)
- Review the API documentation

## Next Steps

- [Basic Bot Tutorial](basic-bot.md)
- [NFT Creation Tutorial](nft-creation.md)
- [Group Chat Integration](group-chat.md)
- [API Reference](../api/telegram.md) 