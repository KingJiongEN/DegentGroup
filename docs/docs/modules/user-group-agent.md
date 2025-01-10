# User Group Agent

The User Group Agent module manages group interactions and user behavior in chat environments.

## Overview

```python
from teleAgent.models.agent_model.user_groupagent import UserGroupAgent
```

The `UserGroupAgent` class extends the base agent functionality to handle group-specific behaviors and interactions.

## Core Components

### State Management

```python
class UserGroupAgent(ProactGroupAgent):
    def __init__(self, name: str, system_message: str, **kwargs):
        super().__init__(name=name, system_message=system_message, **kwargs)
        self.working_memory = {}
        self.long_term_memory = {}
        self.social_relations = {}
```

### Event Handling

```python
async def a_update_inner_state(self, messages, sender, **kwargs):
    """
    Update agent's inner state based on new messages
    
    Args:
        messages: List of message dictionaries
        sender: The agent or user who sent the messages
    """
    if self.working_memory.get('fast_reply', 0):
        self.working_memory.update({'response_decision': 0})
        return (False, None)
        
    message = self.transform_message_history(messages, sender)
    self.update_message_to_modules(message)
    reply = await self.a_initiate_chats(self.module_sequence)
    self.update_system_message()
```

### Social Interaction Management

```python
def update_social_relations(self, user_id: str, interaction_data: dict):
    """
    Update social relationship data for a specific user
    
    Args:
        user_id: Unique identifier for the user
        interaction_data: Dictionary containing interaction metrics
    """
    if user_id not in self.social_relations:
        self.social_relations[user_id] = {}
    
    self.social_relations[user_id].update(interaction_data)
```

## Integration Examples

### Basic Group Chat Setup

```python
async def setup_group_chat():
    agent = UserGroupAgent(
        name="GroupManager",
        system_message="I am a helpful group chat manager",
        llm_config={"model": "gpt-4"}
    )
    
    # Add event handlers
    @agent.on_user_join
    async def welcome_user(user):
        await agent.send_message(
            f"Welcome {user.name} to the group!"
        )
        
    return agent
```

### Advanced Usage

```python
# Implementing complex group behaviors
async def manage_group_dynamics():
    agent = UserGroupAgent(...)
    
    # Monitor and moderate discussions
    @agent.on_message
    async def moderate_content(message):
        analysis = await agent.analyze_message(message)
        if analysis.requires_moderation:
            await agent.moderate_message(message)
            
    # Track user engagement
    @agent.on_interaction
    async def track_engagement(interaction):
        await agent.update_user_metrics(
            interaction.user_id,
            interaction.metrics
        )
```

## Best Practices

1. **State Management**
   - Regularly persist important state data
   - Implement state recovery mechanisms
   - Clear temporary states periodically

2. **Memory Management**
   - Use working memory for short-term context
   - Persist important information to long-term memory
   - Implement memory cleanup routines

3. **Social Relations**
   - Track user interactions
   - Update relationship metrics
   - Use relationship data for personalized responses

4. **Error Handling**
   - Implement graceful fallbacks
   - Log errors appropriately
   - Maintain group stability during errors

## Configuration

```python
agent_config = {
    "name": "GroupManager",
    "personality": "helpful and friendly",
    "response_style": "casual",
    "memory_config": {
        "max_working_memory": 1000,
        "persistence_path": "/path/to/storage"
    },
    "moderation_rules": {
        "max_messages_per_minute": 10,
        "forbidden_words": ["spam", "abuse"],
        "action_thresholds": {
            "warning": 2,
            "mute": 3,
            "ban": 5
        }
    }
}
``` 