# Agent Model System

This module implements a sophisticated agent system with cognitive capabilities, artwork creation, and bargaining abilities. The system is built with a modular architecture that allows for flexible extension and customization.

## Core Components

### GroupChat Agemt

The agent uses a modular cognitive architecture with the following key components:

- **Emotion Module**: Manages agent's emotional states and responses
- **Speech Module**: Handles text-to-speech conversion
- **Pause Module**: Controls conversation flow and timing
- **Reflection Module**: Enables self-reflection and learning
- **Social Relationship Module**: Manages relationships with other agents
- **Thoughts Module**: Handles agent's internal thought processes
- **Summary Module**: Creates summaries of conversations

Every time the agent receive a new message, it will go through all inner modules to update agent's mental states for the final message output.

#### Creating a New Inner Module

To create a new inner module:

1. Create a new class inheriting from `CognitiveModuleAgent`:

```python
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent

class NewModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=YourPromptClass, *args, **kwargs):
        super().__init__(
            name='new_module',
            system_message="Your module's system message",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.your_processing_function)
    
    def your_processing_function(self, message_dict, recipient):
        # Implement your module's logic here
        return dict()
```

2. Define a prompt class for your module:

```python
from teleAgent.models.agent_model.prompts.base_prompt import BasePrompt

class YourPromptClass(BasePrompt):
    def __init__(self):
        super().__init__()
        self.prompt = """Your prompt template"""
        self.response_format = """Expected response format"""
```

### 2. Artwork Creation System

The artwork creation system consists of three main components:

- **CreativeArtistAgent**: Creates artwork based on NFT analysis
- **ArtworkCritic**: Provides critique and feedback
- **DalleDrawer**: Handles image generation

Example usage:

```python
artwork_creator = CreativeArtistAgent(
    character_profile=profile,
    dalle_config=dalle_config,
    llm_config=llm_config,
    wallet_address=wallet_address,
    agent_id=agent_id
)

artwork_result = await artwork_creator.create_complete_artwork(messages)
```

### 3. Bargaining System

The bargaining system implements a multi-agent negotiation process with:

- **Bargainer**: Handles price negotiations
- **Deal Maker**: Manages deal completion
- **Emotion Estimator**: Analyzes user sentiment
- **Bid Estimator**: Predicts likely bids

Example usage:

```python
bargain_agents = create_bargain_group_chat(
    agent_id=agent_id,
    nft_dao=nft_dao,
    artwork_critique_dao=artwork_critique_dao,
    agent_inner_state=agent_inner_state
)

chat_result = await single_round_response(
    bargain_agents,
    context,
    chat_history
)
```

## Bargaining Process

1. **Initial Analysis**
   - Hacking check for security
   - Deal status verification
   - User emotion analysis
   - Bid estimation
   - Purchase intent assessment

2. **Negotiation Flow**
   - Price proposal based on artwork value
   - Response to user counter-offers
   - Deal confirmation and completion
   - NFT transfer handling

3. **Transaction Handling**
   - Wallet address verification
   - Payment confirmation
   - NFT transfer execution

## Artwork Creation Process

1. **Analysis Phase**
   - Analyze NFT features and style
   - Extract key visual elements
   - Determine color schemes

2. **Creation Phase**
   - Generate artwork description
   - Create image using DALL-E
   - Apply artist's style preferences

3. **Review Phase**
   - Critique artwork quality
   - Assess style consistency
   - Generate metadata

## Configuration

The system uses various configuration files for:
- LLM models
- DALL-E integration
- Agent personalities
- Bargaining parameters

See the respective configuration files in the `constant` directory for detailed settings.

## Dependencies

- autogen
- openai
- Pillow
- pydantic
- Other requirements in `requirements.txt`

## Usage

See individual module documentation and example files for detailed usage instructions.
