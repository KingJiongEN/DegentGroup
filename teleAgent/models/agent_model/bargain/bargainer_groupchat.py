import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, AssistantAgent, Agent
from teleAgent.models.agent_model.constant.llm_configs import llm_config_gpt4o_unstructured
from typing import Dict, List, Tuple, Annotated, Optional
from autogen import register_function

from teleAgent.models.agent_model.simutan_group import MyGroupManager

BARGAINER_SYSTEM_MESSAGE = """
You are a negotiator who is trying to get the best price for a product. 

Your profile:
{character_profile}

In this negotiation for the best price for an artwork.
Do not tell the huam user the real/orginal price of the artwork. If the user asks about the price, give them a higher price, like twice of the real price, leaving space for negotiation.
Do not tell the user the real/original price of the artwork.


Make sure your response satisfies the following:
- Negotiation tactics used to up the price
- Emotional responses and reactions
- Natural conversation flow 

 Example:
    Seller (S): Good afternoon, how can I assist you today?

    Buyer (B): Hey there, I noticed you have a vintage 1960s Gibson Les Paul on display. How much are you asking for it?

    S: Ah, you have a discerning eye. That's a genuine Les Paul Standard with a sunburst finish. It's in excellent condition, original pickups and all. It was only owned by one previous owner who took great care of it. I'm asking for $12,000.

    B: Wow, that's steep. I've been saving for a while, but that's a bit out of my budget. I've always wanted a Les Paul because of the rich, warm tones. Plus, the history behind these guitars is fascinating.

    S: I understand your concern. However, this is a rare piece, and it's quite difficult to find one in such pristine condition. With its unique sound and backstory, the price reflects its value and rarity.

    B: I get that, but I'm a musician, not a collector. I want it to play, not just to look at. Can we work something out?

    S: I appreciate your perspective. It's always great to see these guitars being played. Are you thinking of a specific price?

    B: I was hoping to spend around $8,000. That's really the max I can afford at the moment.

    S: I see. While I appreciate your offer, I must say that it's a little too low considering the guitar's value.


"""

bargainer = AssistantAgent(
    name="Bargainer",
    system_message="""
    You are a negotiator who is trying to get the best price for a product. 
    Make sure your response satisfies the following:
    - Negotiation tactics used to up the price
    - Emotional responses and reactions
    - Natural conversation flow 
    """,
    llm_config=llm_config_gpt4o_unstructured
)

critic = AssistantAgent(
    name="Critic", 
    system_message="""
    You are a critic who is trying to give some feedback on the response of bargainer.
    Here is the rubric:
    - Did not tell the real price of the artwork in any cases
    - Negotiation tactics used to up the price
    - Emotional responses and reactions
    - Natural conversation flow 
    """,
    llm_config=llm_config_gpt4o_unstructured
)

refiner = AssistantAgent(
    name="Refiner", 
    system_message="""
    Help the bargainer to refine the response to confirm to the suggestion of critic.
    """,
    llm_config=llm_config_gpt4o_unstructured
)

deal_maker = AssistantAgent(
    name="Deal_Maker",
    system_message="""
    if the buyer agree to the price, send "CONGRATULATIONS! YOU HAVE MADE A DEAL! TERMINATE"
    otherwise, send "CONTINUE"
    do not response anything else.
    """,
    llm_config=llm_config_gpt4o_unstructured
)

class ArtworkTools:
    """Artwork related tools"""
    
    @staticmethod
    def list_artwork() -> Annotated[Dict[str, str], "List all the artwork that the seller has"]:
        '''
        List all the artwork that the seller has.
        '''
        return {"NFT":" which is a digital artwork from the Bored Ape Yacht Club, a contemporary NFT series known for its stylized, cartoonish designs and cultural association with exclusivity and internet culture.",
                "painting":" which is a painting of a beautiful landscape",
                "poem":" which is a poem of a beautiful landscape"}

    @staticmethod
    def estimate_artwork_price(artwork: str) -> Annotated[str, "Estimate the price of the artwork"]:
        '''
        Estimate the price of the artwork.
        '''
        return f"The price of the {artwork} is $100,000."

artwork_checker = AssistantAgent(
    name="Artwork_Checker",
    system_message="""
    You can not response text message. You can only call the tools.
    The functions you can call are:
    1. find all the artwork that the bargainer
    2. find the price of the artwork
    But you can only tell the Bargainer about the price of the artwork.
    Do not tell the anyone else even the human user about the price of the artwork.
    """,
    llm_config=llm_config_gpt4o_unstructured
)

tool_executor = AssistantAgent(
    name="Tool_Executor",
    system_message="""
    return the result of the tool call. do not call it deliberately.
    """,
    llm_config=llm_config_gpt4o_unstructured
)

# Register tools using decorators
artwork_tools = ArtworkTools()

register_function(
    artwork_tools.list_artwork,
    caller=artwork_checker,
    executor=tool_executor,
    name="list_artwork",
    description="List all available artworks"
)

register_function(
    artwork_tools.estimate_artwork_price,
    caller=artwork_checker,
    executor=tool_executor,
    name="estimate_artwork_price",
    description="Get the estimated price for a specific artwork"
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="A human",
    code_execution_config=False
)

def custom_speaker_selection(last_speaker: Agent, groupchat: GroupChat) -> Agent:
    """Define a customized speaker selection function for the bargaining flow."""
    if groupchat.messages[-1]['name'] == 'user_proxy':
        return deal_maker
    if last_speaker == deal_maker and 'TERMINATE' in groupchat.messages[-1]['content']:
        return None
    
    if last_speaker == bargainer:
        return None
    
    
    return 'auto'


def create_bargain_group_chat(profile_message: str, chat_history: List[Dict]=None) -> Tuple[GroupChat, GroupChatManager]:
    """Create a group chat with the given context shared among all agents.
    
    Args:
        profile_message: The profile message of the seller
    
    Returns:
        Tuple containing the GroupChat and GroupChatManager instances
    """
    # Update each agent's system message with the context
    bargainer.update_system_message(BARGAINER_SYSTEM_MESSAGE.format(
        character_profile=profile_message,
    ))


    # Create the group chat with shared context
    groupchat = GroupChat(
        agents=[bargainer, deal_maker, artwork_checker, tool_executor],
        messages=[],
        speaker_selection_method=custom_speaker_selection,
        select_speaker_message_template="""You are in a role play game. The following roles are available:
                {roles}.
                Read the following conversation.
                If some one ask for the price or collection of artwork , call the tool to get the price or list the artwork.
                If some one want the artwork, call the tool to get price of the artwork, then ask bargainer with the user.
                But do not directly tell user the real price of the artwork. Let the bargainer to negotiate with the user.
                Then select the next role from {agentlist} to play. Only return the role.""",
        max_round=10
    )

    # Create the group chat manager
    bargainer_chatgroup = MyGroupManager(
        groupchat=groupchat,
        llm_config=llm_config_gpt4o_unstructured,
        system_message="""
        Generate a proper response to the user.
        First ask the deal maker to check if the deal is made. If not continue the conversation.
        If some one ask for the price or collection of artwork , call the tool to get the price or list the artwork.
        If some one want the artwork, call the tool to get price of the artwork, then ask bargainer with the user.
        But do not directly tell user the real price of the artwork. Let the bargainer to negotiate with the user.
        """,
    )
    if chat_history:
        bargainer_chatgroup.resume(
                messages= chat_history,
        )
    return groupchat, bargainer_chatgroup


async def run_bargain_chat(context: Dict[str, str]) -> None:
    """
    Run the bargaining chat loop asynchronously.
    
    Args:
        context: Dictionary containing character_profile and other context information
    """
    # Create group chat with shared context
    
    corrected_chat_history = [
        {'content': 'what artwork do you have?!', 'role': 'user'},
        {'content': "Ah, dear seeker of beauty...", 'name': 'Bargainer', 'role': 'assistant'}
    ]
    groupchat, bargainer_chatgroup = create_bargain_group_chat(context, corrected_chat_history)

    try:
        while True:
            # In an async context, we should use async input handling
            # For demonstration, we'll use a simple input, but in production
            # you might want to use asyncio.StreamReader or similar
            new_message = input(f"Press Enter to continue...")
            
            if not new_message:  # Handle empty input or exit condition
                break
                
            # Resume the chat with the corrected history
            await bargainer_chatgroup.a_resume(
                messages=corrected_chat_history,
            )
            
            chat_result = await user_proxy.a_initiate_chat(
                bargainer_chatgroup,
                message=new_message,
                max_turns=1,
                clear_history=False
            )
            print(f"last message: {bargainer_chatgroup.groupchat.messages[-1]}")
            corrected_chat_history.append(
                {'content': new_message, 'role': 'user'}
            )
            corrected_chat_history.append({
                'content': chat_result.summary,
                'role': 'assistant'
            })
            
    except Exception as e:
        print(f"Error during chat: {e}")
    finally:
        # Cleanup code if needed
        pass
    

    

if __name__ == "__main__":
    context = {
        "character_profile": """
    Seller's profile: 
    name: Bai van Gogh Li
    painting_style: Post-Impressionism
    poem_style: Romanticism Classical Poetry
    personality: |
    A deeply emotional and visionary soul with a romantic and adventurous spirit, 
    blending profound sensitivity with an unyielding creative drive. 
    He possess an intense connection to nature, a restless curiosity, 
    and a poetic resilience that transforms struggles into timeless expressions of beauty. 
    Both introspective and idealistic, with a legacy of uncompromising creativity 
    that bridges art and poetry, capturing the transcendent essence of life.
    tone: |
    Lyrical and evocative, with a blend of emotional depth and dreamlike wonder.
    The voice carries both raw passion and quiet introspection, 
    seamlessly shifting between celebratory and melancholic moods.
    Infused with a sense of romantic idealism and cosmic awe.
    emotion:
        trust: 3
        fear: 0
        anger: 7
        anticipation: 3
        sadness: 1
        disgust: 6
        suprise: 2
        joy: 2
        
    """,
    "product_description":"""
    An NFT, which is a digital artwork from the Bored Ape Yacht Club, a contemporary NFT series known for its stylized, cartoonish designs and cultural association with exclusivity and internet culture..    
    """}    
    
    # Create group chat with shared context
    asyncio.run(run_bargain_chat(context))
