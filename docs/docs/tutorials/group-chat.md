# Group Chat Integration Tutorial

This tutorial will guide you through implementing advanced group chat features using TeleAgent's User Group Agent.

## Overview

We'll implement:
1. Advanced group chat management
2. Multi-user conversation handling
3. Role-based permissions
4. Group memory and context management
5. Proactive interactions

## Prerequisites

- Completed [Basic Bot Setup](basic-bot.md)
- Understanding of TeleAgent's User Group Agent
- Basic knowledge of Telegram group features

## Project Structure

```
group_bot/
├── handlers/
│   ├── group_handler.py
│   ├── admin_handler.py
│   └── memory_handler.py
├── models/
│   ├── group_state.py
│   └── user_state.py
├── utils/
│   └── permissions.py
└── main.py
```

## Step 1: Group Chat Setup

```python
# handlers/group_handler.py
from teleAgent.models.agent_model.user_groupagent import UserGroupAgent
from teleAgent.models.memory import GroupMemory

class GroupChatHandler:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.agent = UserGroupAgent(
            name="GroupManager",
            system_message="I am a helpful group chat manager",
            memory_config={
                "max_history": 1000,
                "persistence": True
            }
        )
        self.memory = GroupMemory()
        
    async def setup(self):
        @self.client.on_new_chat_members()
        async def handle_new_members(message):
            for user in message.new_chat_members:
                await self._welcome_user(message.chat.id, user)
                await self._update_group_state(message.chat.id, "new_member")
                
        @self.client.on_left_chat_member()
        async def handle_left_member(message):
            await self._handle_member_left(
                message.chat.id,
                message.left_chat_member
            )
            
    async def _welcome_user(self, chat_id: int, user):
        welcome_message = await self.agent.generate_welcome_message(user)
        await self.client.send_message(
            chat_id=chat_id,
            text=welcome_message
        )
```

## Step 2: Role-Based Permissions

```python
# utils/permissions.py
from enum import Enum
from functools import wraps

class UserRole(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"
    GUEST = "guest"

class PermissionManager:
    def __init__(self):
        self.role_permissions = {
            UserRole.ADMIN: {"can_manage", "can_moderate", "can_post"},
            UserRole.MODERATOR: {"can_moderate", "can_post"},
            UserRole.MEMBER: {"can_post"},
            UserRole.GUEST: set()
        }
        
    def requires_permission(self, permission: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(message, *args, **kwargs):
                user_role = await self.get_user_role(message.from_user.id)
                if permission in self.role_permissions[user_role]:
                    return await func(message, *args, **kwargs)
                else:
                    await message.reply(
                        "You don't have permission to perform this action."
                    )
            return wrapper
        return decorator
```

## Step 3: Group Memory Management

```python
# models/group_state.py
from datetime import datetime

class GroupState:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.members = {}
        self.conversation_history = []
        self.active_topics = set()
        self.last_activity = datetime.now()
        
    async def update_conversation(self, message: dict):
        """Update conversation history and analyze context"""
        self.conversation_history.append({
            "user_id": message["from_user"]["id"],
            "text": message["text"],
            "timestamp": datetime.now(),
            "context": await self._analyze_context(message)
        })
        
        # Cleanup old history if needed
        if len(self.conversation_history) > 1000:
            self.conversation_history = self.conversation_history[-1000:]
            
    async def _analyze_context(self, message: dict) -> dict:
        """Analyze message context using the agent"""
        return await self.agent.analyze_message_context(message)
```

## Step 4: Proactive Interactions

```python
# handlers/proactive_handler.py
class ProactiveHandler:
    def __init__(self, client: TelegramClient, agent: UserGroupAgent):
        self.client = client
        self.agent = agent
        self.cooldown = 300  # 5 minutes
        
    async def setup(self):
        # Schedule periodic checks
        asyncio.create_task(self._periodic_check())
        
    async def _periodic_check(self):
        while True:
            for group in self.agent.active_groups:
                await self._check_group_activity(group)
            await asyncio.sleep(self.cooldown)
            
    async def _check_group_activity(self, group_id: int):
        state = await self.agent.get_group_state(group_id)
        
        # Check for inactive conversations
        if await self._should_initiate_conversation(state):
            topic = await self.agent.generate_topic(state)
            await self.client.send_message(
                chat_id=group_id,
                text=f"💭 {topic}"
            )
```

## Step 5: Advanced Message Handling

```python
# handlers/message_handler.py
class MessageHandler:
    def __init__(self, client: TelegramClient, agent: UserGroupAgent):
        self.client = client
        self.agent = agent
        
    async def setup(self):
        @self.client.on_message()
        async def handle_message(message):
            # Update group state
            await self.agent.update_group_state(message)
            
            # Check if should respond
            if await self._should_respond(message):
                response = await self.agent.generate_response(message)
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=response
                )
                
    async def _should_respond(self, message) -> bool:
        """Determine if the agent should respond to the message"""
        # Check if message is directed to the bot
        if message.reply_to_message and \
           message.reply_to_message.from_user.id == self.client.id:
            return True
            
        # Check if bot is mentioned
        if f"@{self.client.username}" in message.text:
            return True
            
        # Use agent to determine if response is needed
        return await self.agent.should_respond(message)
```

## Step 6: Main Application Integration

```python
# main.py
async def main():
    # Initialize client
    client = TelegramClient(config)
    
    # Initialize agent
    agent = UserGroupAgent(
        name="GroupManager",
        system_message="I am a helpful group chat manager",
        llm_config={"model": "gpt-4"}
    )
    
    # Setup handlers
    group_handler = GroupChatHandler(client)
    proactive_handler = ProactiveHandler(client, agent)
    message_handler = MessageHandler(client, agent)
    
    await group_handler.setup()
    await proactive_handler.setup()
    await message_handler.setup()
    
    # Start the bot
    await client.start()
    await client.run_forever()
```

## Best Practices

1. **Memory Management**
   ```python
   # Implement periodic cleanup
   async def cleanup_old_data():
       while True:
           await agent.cleanup_memory()
           await asyncio.sleep(3600)  # Every hour
   ```

2. **Rate Limiting**
   ```python
   # Implement group-specific rate limits
   rate_limiter = RateLimiter(
       max_requests=5,
       time_window=60,
       per_chat=True
   )
   ```

3. **Error Recovery**
   ```python
   # Implement state recovery
   async def recover_state():
       try:
           return await load_persisted_state()
       except Exception:
           return await create_new_state()
   ```

## Testing

```python
# test_group_chat.py
@pytest.mark.asyncio
async def test_group_chat_handling():
    # Mock setup
    client = AsyncMock()
    agent = AsyncMock()
    
    # Test message handling
    handler = MessageHandler(client, agent)
    message = create_test_message()
    await handler.handle_message(message)
    
    # Verify response
    agent.generate_response.assert_called_once()
```

## Troubleshooting

1. **Message Processing Issues**
   - Check message format
   - Verify bot permissions
   - Monitor rate limits

2. **Memory Issues**
   - Monitor memory usage
   - Implement cleanup routines
   - Use persistent storage

3. **Performance Issues**
   - Implement caching
   - Use batch processing
   - Optimize database queries

## Next Steps

1. Add advanced features:
   - Voice message handling
   - Poll management
   - Event scheduling

2. Implement analytics:
   - User engagement metrics
   - Response quality tracking
   - Performance monitoring

3. Explore other tutorials:
   - [Bargaining System](bargaining-system.md)
   - [Artwork Creation](artwork-creation.md) 