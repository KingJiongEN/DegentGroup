# Agent Model System

This module implements a sophisticated agent system with cognitive capabilities, artwork creation, and bargaining abilities. The system is built with a modular architecture that allows for flexible extension and customization.

## Core Components

### 1. Proactive Group Agent

The `ProactGroupAgent` class extends `AssistantAgent` and implements a proactive agent that can:
- Participate in group chats
- Maintain emotional states
- Process messages through cognitive modules
- Generate contextual responses

Key features:
- Group chat management
- Message history transformation
- Inner state updates
- Timestamp-based message tracking

### 2. Inner Modules

#### Core Inner Modules
Each module serves a specific cognitive function:

```python
class ProactGroupAgent(AssistantAgent, Agent):
    def __init__(self, *args, **kwargs):
        # Initialize inner modules
        self.emotion_module = EmotionModuleAgent()
        self.social_module = SocialRelationshipModuleAgent()
        self.thoughts_module = ThoughtsModuleAgent()
        self.summary_module = SummaryModuleAgent()
        self.reflection_module = ReflectInteractionModuleAgent()
```

#### Creating Custom Inner Modules

1. Create a new module class:

```python
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent

class CustomModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=CustomPrompt, *args, **kwargs):
        super().__init__(
            name='custom_module',
            system_message="Your module's system message",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.process_message)
    
    def process_message(self, message_dict, recipient):
        # Implement module logic
        return {"processed_data": message_dict}
```

2. Define module prompt:

```python
from teleAgent.models.agent_model.prompts.base_prompt import BasePrompt

class CustomPrompt(BasePrompt):
    def __init__(self):
        super().__init__(prompt_type='custom')
        self.recordable_key = ['key1', 'key2']
        self.format_prompt = """
        Your prompt template here.
        Expected output format:
        {
            "key1": "value1",
            "key2": "value2"
        }
        """
```

3. Integrate with ProactGroupAgent:

```python
class ProactGroupAgent(AssistantAgent, Agent):
    def __init__(self, *args, **kwargs):
        # Add custom module
        self.custom_module = CustomModuleAgent(
            llm_config=self.llm_config
        )
        self.inner_modules.append(self.custom_module)
```

#### Module Processing Flow

1. Message Reception:
```python
async def process_message(self, message):
    for module in self.inner_modules:
        processed = await module.process(message)
        self.update_state(processed)
```

2. State Updates:
```python
def update_state(self, module_output):
    self.working_memory.update(module_output)
    self.update_system_message()
```

### 3. System Messages

The agent uses dynamic system messages that incorporate:
- Agent profile
- Personality traits
- Art preferences
- Current emotional state
- Interaction patterns

Example system message template:
```python
PROFILE_MESSAGE = """
    You are {self.name}. {self.chat_situation_prompt}
    Your personality is: {self.personality}
    Your painting style is: {self.painting_style}
    Your tone is: {self.tone}
    Your art preference is: {self.art_preference}
    Your current mood is: {self.emotion}
"""
```

## Usage

For detailed usage instructions and examples, refer to individual module documentation and the example files in the project repository.