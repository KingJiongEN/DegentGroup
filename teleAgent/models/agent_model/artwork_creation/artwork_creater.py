import asyncio
from typing import Dict, List, Any, Union
import uuid
from autogen import AssistantAgent, ConversableAgent
from autogen.agentchat.contrib.capabilities import generate_images
from autogen.agentchat.contrib.capabilities.vision_capability import VisionCapability
from autogen.agentchat.contrib import img_utils
from PIL.Image import Image
import os
import logging
from dataclasses import dataclass
from pathlib import Path


from teleAgent.constants import IMAGE_FILE_NAME_FORMAT
from teleAgent.models.agent_model.artwork_creation.dalle_draw import dalle_draw
from teleAgent.models.agent_model.constant.llm_configs import llm_config_gpt4o_unstructured, dalle_config
from teleAgent.models.agent_model.utilities.small_tools import extract_json_from_markdown
from teleAgent.models.nft import NFTMetadata
from teleAgent.plugins.plugin_solana.tools.create_nft import NFTCreationResult, create_nft_with_generation
from teleAgent.models.agent_model.utilities.small_tools import get_base64_image

@dataclass
class ArtworkCreationResult:
    token_id: str
    name: str
    description: str
    url: str
    nft_metadata: NFTMetadata
    art_style: str = "Unknown"
    attributes: List[Dict[str, Any]] = None
    

class CreativeArtistAgent:
    """An agent that analyzes NFTs, generates poetry, and creates artwork"""
    
    def __init__(
        self,
        character_profile: Union[dict,str],
        dalle_config: dict,
        llm_config: dict,
        wallet_address: str,
        agent_id: str,
    ):
        # Initialize sub-agents for specialized tasks
        self.analyzer = self._create_analyzer_agent(llm_config)
        self.critic = self._create_critic_agent(llm_config)
        self.artist = self._create_artist_agent(character_profile, dalle_config, llm_config)
        
        self.critic_msg= '''
                PAINTING_STYLE: {painting_style},
                NFT_ANALYSIS: {nft_analysis},
                the current prompt is: {current_prompt}
        '''
        
        self.character_profile = character_profile
        self.wallet_address = wallet_address
        self.agent_id = agent_id
        
    def _create_analyzer_agent(self, llm_config: dict) -> AssistantAgent:
        """Creates an agent specialized in analyzing NFT features"""
        analyzer = AssistantAgent(
            name="NFTAnalyzer",
            system_message="""You are an expert NFT analyst. Analyze images and text to:
            1. Identify key visual elements and traits
            2. Extract color schemes and artistic style
            3. Note any unique or distinctive features
            4. Summarize the overall theme and mood
            Provide analysis in a structured format.""",
            llm_config=llm_config
        )
        
        # Add vision capability to the analyzer
        # vision_capability = VisionCapability(
        #     lmm_config=llm_config,
        # )
        # vision_capability.add_to_agent(analyzer)
        
        return analyzer

    def _create_poet_agent(self, profile: dict, llm_config: dict) -> AssistantAgent:
        """Creates an agent specialized in poetry generation"""
        return AssistantAgent(
            name="Poet",
            system_message=f"""You are a poet with the following style and personality:
            {profile}
            Create poems that blend NFT characteristics with your unique voice.""",
            llm_config=llm_config
        )

    def _create_critic_agent(self,  llm_config: dict) -> AssistantAgent:
        """Creates an agent specialized in artwork criticism"""
        critic_prompt = f"""You need to improve the prompt to dalle to generate the NFT artwork.
        To ensure the prompted dalle generated artwork follows the keypoints of the painting style and the nft analysis. Make sure the main character face towards the right.
        you will be given the following information:
        PAINTING_STYLE, NFT_ANALYSIS and the current prompt.
        return the improved prompt without any other text.
        """
        
        critic = AssistantAgent(
            name="Critic",
            system_message=critic_prompt,
            llm_config=llm_config
        )
        return critic

    def _create_artist_agent(self, profile: dict, dalle_config: dict, llm_config: dict) -> AssistantAgent:
        """Creates an agent specialized in artwork generation"""
        artist = AssistantAgent(
            name="Artist",
            system_message=f"""You are an artist with the following style:
            {profile}
            Create artwork that fuses NFT elements with your distinctive style.""",
            llm_config=llm_config,
        )
        
        # Add DALL-E image generation capability
        # dalle_gen = generate_images.DalleImageGenerator(llm_config=dalle_config)
        # image_gen = generate_images.ImageGeneration(
        #     image_generator=dalle_gen,
        #     text_analyzer_llm_config=llm_config
        # )
        # image_gen.add_to_agent(artist)
        
        return artist

    async def analyze_nft_features(self, messages: List[Dict]) -> str:
        """Analyze NFT features from conversation history"""
        # Extract images and prepare message content
        image_contents = []
        for message in messages:
            if isinstance(message.get("content"), list):
                for content in message["content"]:
                    if isinstance(content, dict) and content.get("type") == "image_url":
                        image_url = content["image_url"]["url"]
                        if image_url.startswith("data:image/jpeg;base64,"):
                            image_contents.append(content)
                        elif Path(image_url).exists():
                            base64_image = get_base64_image(str(image_url))
                            image_contents.append({
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            })
        
        # Create analysis prompt with both text and images
        analysis_prompt = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Please analyze these NFT elements:
                    Provide a structured analysis of key features, style, and themes."""
                },
                *image_contents  # Unpack all image contents
            ]
        }
        
        # Get analysis from analyzer agent
        analysis = await self.critic.a_initiate_chat(recipient=self.analyzer, message=analysis_prompt, max_turns=1, silent=True) # poet as user
        return analysis.summary

    async def create_fusion_artwork(self, nft_analysis: str) -> ArtworkCreationResult:
        """Create artwork combining NFT features with character's style"""
        art_prompt = f"""
        Create an artwork that fuses these elements:
        
        NFT Analysis:
        {nft_analysis}
        
        Artistic Style:
        {self.character_profile}
        
        Create a harmonious blend of the NFT's key features and your signature style,
        make sure the description contains the key features of the NFT and the painting style of the character.
        the response should be a json object with the following fields that can guide the dalle to generate the artwork:
        limit the description length to 600 words.
        {{
            "name": str,
            "description": str,
            "art_style": str,
            "attributes": dict,
        }}
        note that in the description, the main character face towards the right
        """
        
        try:
            basic_response = await self.critic.a_initiate_chat(recipient=self.artist, message=art_prompt, max_turns=1, silent=True)
            
            if not basic_response or not basic_response.summary:
                raise ValueError("No response received from artist agent")
            
            response_dict = eval(extract_json_from_markdown(basic_response.summary))
            if not all(key in response_dict for key in ["name", "description", "art_style", "attributes"]):
                raise ValueError("Invalid response format from artist agent")
            
            improved_response = await self.critic.a_initiate_chat(recipient=self.critic, 
                                                                  message=self.critic_msg.format(painting_style=self.character_profile.get('art_style', ''),
                                                                                                  nft_analysis=nft_analysis,
                                                                                                  current_prompt=response_dict["description"]), 
                                                                  max_turns=1, silent=True)
            
            if not improved_response or not improved_response.summary:
                raise ValueError("No response received from critic agent")
            
            improved_description = improved_response.summary
            response_dict.update({"description": improved_description})
            
            # Generate image using DALL-E
            nft_metadata = NFTMetadata(
                name=response_dict["name"],
                description=improved_description,
                image_url=None,
                art_style=response_dict["art_style"],
                attributes=response_dict["attributes"],
            )
            
            if os.getenv('DEBUG'):
                url = dalle_draw(improved_description)
                assert url, "Failed to generate image"
                nft_metadata.image_url = url
                token_id = uuid.uuid4()
            else:
                creation_result:NFTCreationResult = await create_nft_with_generation( wallet_address=self.wallet_address,
                                                                    name=response_dict["name"],
                                                                    prompt=improved_description, 
                                                                    metadata=nft_metadata,
                                                                    creator_id=self.wallet_address
                                                                )
                nft_metadata.image_url = creation_result.image_url

                if not creation_result.success:
                    raise ValueError("Failed to generate image")
                else:
                    logging.info(f"NFT creation success: {creation_result}")
                    token_id = creation_result.token_id
            
            return ArtworkCreationResult(
                token_id=token_id,
                name=response_dict["name"],
                description=improved_description,
                art_style=response_dict["art_style"],
                attributes=response_dict["attributes"],
                url=nft_metadata.image_url,
                nft_metadata=nft_metadata
            )
        except Exception as e:
            logging.error(f"Error in create_fusion_artwork: {str(e)}")
            raise
     

    def _extract_images(self, messages: List[Dict]) -> List[Image]:
        """Extract images from message history"""
        images = []
        for message in messages:
            if isinstance(message.get("content"), list):
                for content in message["content"]:
                    if isinstance(content, dict) and content.get("type") == "image_url":
                        img_data = content["image_url"]["url"]
                        images.append(img_utils.get_pil_image(img_data))
        return images

    def _extract_text(self, messages: List[Dict]) -> str:
        """Extract text content from message history"""
        text_content = []
        for message in messages:
            if isinstance(message.get("content"), str):
                text_content.append(message["content"])
            elif isinstance(message.get("content"), list):
                for content in message["content"]:
                    if isinstance(content, dict) and content.get("type") == "text":
                        text_content.append(content["text"])
        return " ".join(text_content)

    async def create_complete_artwork(self, messages: List[Dict]) -> ArtworkCreationResult:
        """Complete process of analyzing, poetizing, and creating artwork"""
        # Analyze NFT features
        nft_analysis = await self.analyze_nft_features(messages)
        
        # Create fusion artwork
        artwork_dict = await self.create_fusion_artwork(nft_analysis)
        drawing = img_utils.get_pil_image(artwork_dict.url)
        os.makedirs("images", exist_ok=True)
        token_id = artwork_dict.token_id
        local_image_path = f"images/{IMAGE_FILE_NAME_FORMAT.format(uuid=token_id)}"
        drawing.save(local_image_path)
        
        nft_metadata = artwork_dict.nft_metadata
        
        return {
            "name": nft_metadata.name,
            "description": nft_metadata.description,
            "image_url": nft_metadata.image_url,
            "local_image_path": local_image_path,
            "art_style": nft_metadata.art_style,
            "attributes": nft_metadata.attributes,
            "background_story": '',
            "creation_context": nft_analysis,  # Using analysis as creation context
            "analysis": nft_analysis,
            "poem": '',
            "drawing": drawing,
            "token_id": token_id,
            "nft_metadata": nft_metadata
            }
        
def create_artwork_agent(character_profile:Union[dict,str],wallet_address:str,agent_id:str):
    return CreativeArtistAgent(character_profile, dalle_config, llm_config_gpt4o_unstructured, wallet_address,agent_id)

if __name__ == "__main__":
    import yaml
    
    character_profile = yaml.safe_load(open(f'teleAgent/characters/SalvadorDalí.yaml'))
    assert type(character_profile) == dict and 'painting_style' in character_profile
    # Create the artwork creator agent
    artwork_creator = create_artwork_agent(character_profile, character_profile['wallet_address'], character_profile['uid'])

    # load image and message history 
    import os
    import pandas as pd
    import random
    
    topic = os.environ.get('TOPIC', 'BAYC')
    topic_content = yaml.safe_load(open(f'teleAgent/topics/{topic}.yaml'))['content']
    image_folder = yaml.safe_load(open(f'teleAgent/topics/{topic}.yaml'))['image_folder']
    image_ls = Path(image_folder).glob('*.png')
    random.seed(42)
    random_images = random.sample(list(image_ls),k=1)
    print(f"random_images: {random_images}")
    
    def create_welcome_message(random_images):
        return_ls = [
            {
                "type": "text",
                "text": f"Hello, welcome to the art salon. Today's topic is {topic}. "
            },
        ]
        
        for image_path in random_images:
            base64_image = get_base64_image(str(image_path))
            return_ls.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        return return_ls
    # Generate artwork based on chat history
    
    df = pd.read_csv('data_record/2024-12-14 00:45:25/groupchat.csv')[['role', 'content']]
    messages = df.to_dict(orient='records')
    
    welcome_message = create_welcome_message(random_images)
    messages=[
                {'role': "BaivanGoghLi", 
                    'content': welcome_message
                } 
            ] + messages
    artwork = asyncio.run(artwork_creator.create_complete_artwork(messages))
    if artwork:
        print(artwork)
        artwork['drawing'].save("generated_artwork.png")
