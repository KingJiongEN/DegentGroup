# Agent Model API Reference

Comprehensive documentation for the TeleAgent Agent Model system, which handles AI agent behaviors and interactions.

## UserGroupAgent

The main class for managing group chat interactions and user behavior.

### Constructor

```python
def __init__(
    self,
    name: str,
    system_message: str,
    llm_config: dict = None,
    memory_config: dict = None,
    **kwargs
):
    """
    Initialize UserGroupAgent.
    
    Args:
        name (str): Name of the agent
        system_message (str): Base system message defining agent behavior
        llm_config (dict, optional): LLM configuration containing:
            - model (str): Model name (e.g., "gpt-4")
            - temperature (float): Response randomness
            - max_tokens (int): Maximum response length
        memory_config (dict, optional): Memory configuration containing:
            - max_history (int): Maximum conversation history
            - persistence (bool): Whether to persist memory
            
    Raises:
        ValueError: If required parameters are invalid
        ConfigurationError: If configuration is invalid
    """
```

### Core Methods

#### State Management

```python
async def a_update_inner_state(
    self,
    messages: List[dict],
    sender: str,
    **kwargs
) -> Tuple[bool, Optional[str]]:
    """
    Update agent's inner state based on new messages.
    
    Args:
        messages: List of message dictionaries
        sender: The agent or user who sent the messages
        **kwargs: Additional keyword arguments
        
    Returns:
        Tuple containing:
            - bool: Whether to generate a response
            - Optional[str]: Generated response if any
            
    Raises:
        StateUpdateError: If state update fails
    """

async def update_system_message(self) -> None:
    """
    Update agent's system message based on current state.
    
    This method should be called after significant state changes
    to ensure the agent's behavior remains consistent with its
    current state and context.
    """
```

#### Message Processing

```python
async def process_message(
    self,
    message: dict,
    context: dict = None
) -> Optional[str]:
    """
    Process incoming message and generate response.
    
    Args:
        message: Message dictionary containing:
            - text (str): Message text
            - from_user (dict): Sender information
            - chat (dict): Chat information
        context: Additional context information
        
    Returns:
        Optional[str]: Generated response if any
        
    Raises:
        ProcessingError: If message processing fails
    """

async def analyze_message_context(
    self,
    message: dict
) -> dict:
    """
    Analyze message context for better understanding.
    
    Args:
        message: Message to analyze
        
    Returns:
        dict: Context analysis containing:
            - intent (str): Detected message intent
            - sentiment (float): Message sentiment score
            - entities (list): Detected entities
            - topics (list): Detected topics
    """
```

### Memory Management

```python
class Memory:
    def __init__(self, config: dict):
        """
        Initialize memory system.
        
        Args:
            config: Memory configuration containing:
                - max_size (int): Maximum memory size
                - ttl (int): Time-to-live for memories
                - storage_path (str): Path for persistent storage
        """
        
    async def add_memory(
        self,
        key: str,
        value: Any,
        ttl: int = None
    ) -> None:
        """
        Add item to memory.
        
        Args:
            key: Memory identifier
            value: Data to store
            ttl: Optional custom time-to-live
            
        Raises:
            MemoryError: If storage fails
        """
        
    async def get_memory(
        self,
        key: str
    ) -> Optional[Any]:
        """
        Retrieve item from memory.
        
        Args:
            key: Memory identifier
            
        Returns:
            Optional[Any]: Stored value if found
        """
        
    async def cleanup(self) -> None:
        """
        Remove expired memories and optimize storage.
        """
```

### Social Relations

```python
class SocialRelations:
    def __init__(self):
        self.relations = {}
        
    async def update_relation(
        self,
        user_id: str,
        metrics: dict
    ) -> None:
        """
        Update social relationship metrics.
        
        Args:
            user_id: User identifier
            metrics: Relationship metrics containing:
                - trust (float): Trust score
                - familiarity (float): Familiarity level
                - rapport (float): Rapport score
        """
        
    async def get_relation(
        self,
        user_id: str
    ) -> dict:
        """
        Get relationship metrics for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            dict: Current relationship metrics
        """
```

### Emotion Module

```python
class EmotionModule:
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_history = []
        
    async def process_emotion(
        self,
        message: dict
    ) -> str:
        """
        Process message to determine emotional response.
        
        Args:
            message: Message to analyze
            
        Returns:
            str: Determined emotion
        """
        
    async def get_emotional_state(self) -> dict:
        """
        Get current emotional state.
        
        Returns:
            dict: Emotional state containing:
                - current (str): Current emotion
                - intensity (float): Emotion intensity
                - history (list): Recent emotion history
        """
```

### Usage Examples

#### Basic Agent Setup

```python
from teleAgent.models.agent_model.user_groupagent import UserGroupAgent

# Initialize agent
agent = UserGroupAgent(
    name="GroupAssistant",
    system_message="I am a helpful and friendly group chat assistant",
    llm_config={
        "model": "gpt-4",
        "temperature": 0.7
    },
    memory_config={
        "max_history": 1000,
        "persistence": True
    }
)

# Process message
response = await agent.process_message({
    "text": "Hello, how are you?",
    "from_user": {"id": "123", "name": "User"},
    "chat": {"id": "456", "type": "group"}
})
```

#### Advanced State Management

```python
# Update agent state
state_update = await agent.a_update_inner_state(
    messages=[{
        "text": "Let's discuss the project",
        "from_user": {"id": "123", "name": "User"}
    }],
    sender="user"
)

if state_update[0]:  # Should respond
    response = state_update[1]
    # Send response to chat
```

#### Memory Usage

```python
# Store conversation context
await agent.memory.add_memory(
    key="conversation_123",
    value={
        "topic": "Project Discussion",
        "participants": ["User1", "User2"],
        "key_points": ["Deadline", "Budget"]
    },
    ttl=3600  # 1 hour
)

# Retrieve context later
context = await agent.memory.get_memory("conversation_123")
```

### Error Handling

```python
class AgentError(Exception):
    """Base exception for agent-related errors"""
    pass

class StateError(AgentError):
    """Exception for state management errors"""
    pass

class ProcessingError(AgentError):
    """Exception for message processing errors"""
    pass

class MemoryError(AgentError):
    """Exception for memory-related errors"""
    pass

try:
    await agent.process_message(message)
except StateError as e:
    logger.error(f"State error: {e}")
    # Implement state recovery
except ProcessingError as e:
    logger.error(f"Processing error: {e}")
    # Fallback to safe response
except AgentError as e:
    logger.error(f"Agent error: {e}")
    # Handle other errors
``` 