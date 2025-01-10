import logging
from typing import Dict, List
from datetime import datetime
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.vision_capability import VisionCapability
from autogen.agentchat.contrib.img_utils import gpt4v_formatter
from pydantic import BaseModel, Field

from teleAgent.models.agent_model.constant.llm_configs import llm_config_gpt4o_unstructured
from teleAgent.models.agent_model.utilities.small_tools import get_base64_image, extract_json_from_markdown
from teleAgent.constants import TIMESTAMP_FORMAT

class CritiqueDetails(BaseModel):
    style_match: str
    style_match_score: int = Field(ge=0, le=10)
    emotional_impact: str
    emotional_impact_score: int = Field(ge=0, le=10)
    harmony: str
    harmony_score: int = Field(ge=0, le=10)
    areas_for_improvement: str

    def dict(self, *args, **kwargs):
        # Convert to dictionary and ensure all values are JSON serializable
        return {
            "style_match": self.style_match,
            "style_match_score": self.style_match_score,
            "emotional_impact": self.emotional_impact,
            "emotional_impact_score": self.emotional_impact_score,
            "harmony": self.harmony,
            "harmony_score": self.harmony_score,
            "areas_for_improvement": self.areas_for_improvement
        }

class ArtworkCritiqueBase(BaseModel):
    critique_details: Dict
    overall_score: float = Field(ge=0, le=10)
    timestamp: datetime

class CreativeArtCritic:
    """Agent specialized in art criticism based on personality and preferences with vision capability"""
    
    def __init__(self, art_values: Dict, name: str = "Art_Critic"):
        self.art_values = art_values
        
        # Initialize the critic agent with personality-driven system message
        self.critic_agent = AssistantAgent(
            name=name,
            system_message=self._build_system_message(),
            llm_config=llm_config_gpt4o_unstructured
        )
        
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            system_message="A human requesting art critique",
            code_execution_config=False
        )
        
        # Add vision capability to the critic agent
        # vision_capability = VisionCapability(lmm_config=llm_config_gpt4o_unstructured)
        # vision_capability.add_to_agent(self.critic_agent)

    def _build_system_message(self) -> str:
        """Build system message based on personality and preferences"""
        return f"""You are an art critic with the following characteristics:
        
        Personality: {self.art_values['personality']}
        Artistic Preferences: {self.art_values['art_preference']}
        
        When critiquing artwork:
        1. Consider both technical execution and emotional resonance
        2. Maintain your unique perspective and personality
        3. Reference your artistic preferences when relevant
        4. Provide balanced feedback highlighting both strengths and areas for growth
        5. Consider the relationship between the visual elements and the accompanying poem
        6. Analyze the visual elements including composition, color, technique, and style
        """

    def _add_image_to_message(self, message: str, image_url: str) -> List[Dict]:
        """Add image to the message to conform to gpt4v format"""
        try:
            # Handle both local file paths and URLs
            if image_url.startswith(('http://', 'https://')):
                base64_image = get_base64_image(image_url)
            else:
                # For local files, read directly
                with open(image_url, 'rb') as image_file:
                    import base64
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
         
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {"type": "text", "text": message},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ]
            return messages
        except Exception as e:
            logging.error(f"Error processing image: {str(e)}")
            raise
        
        
    async def critique_artwork(self, artwork_dict: Dict) -> ArtworkCritiqueBase:
        """Generate a critique for the given artwork"""
        if not artwork_dict or not isinstance(artwork_dict, dict):
            raise ValueError("Invalid artwork dictionary provided")
            
        required_fields = ['name', 'description', 'art_style', 'poem', 'drawing']
        missing_fields = [field for field in required_fields if field not in artwork_dict]
        if missing_fields:
            raise ValueError(f"Missing required fields in artwork dictionary: {missing_fields}")
            
        critique_prompt = f"""Please critique this artwork based on your artistic perspective:
        
        Title: {artwork_dict['name']}
        Description: {artwork_dict['description']}
        Style: {artwork_dict['art_style']}
        
        Consider:
        - How the style aligns with your artistic preferences
        - The emotional impact and technical execution
        - The harmony between the visual elements and the poem
        - Areas of strength and potential improvement
        - The visual composition, color palette, and technical execution
        
        return a json with the following keys:
        {{
            "style_match": str,
            "style_match_score": int,
            "emotional_impact": str,
            "emotional_impact_score": int,
            "harmony": str,
            "harmony_score": int,
            "areas_for_improvement": str,
        }}
        """
        
        try:
            messages = self._add_image_to_message(critique_prompt, artwork_dict['local_image_path'])
            chat_result = await self.critic_agent.a_generate_reply(
                messages,
                sender=self.user_proxy
            )
            
            if not chat_result:
                raise ValueError("No response received from critic agent")
                
            response_dict = eval(extract_json_from_markdown(chat_result))
            if not all(key in response_dict for key in [
                'style_match_score', 'emotional_impact_score', 'harmony_score'
            ]):
                raise ValueError("Invalid critique format received")
                
            overall_score = sum([
                response_dict['style_match_score'],
                response_dict['emotional_impact_score'],
                response_dict['harmony_score']
            ]) / 3.0

            critique_details = CritiqueDetails(**response_dict)
            
            return ArtworkCritiqueBase(
                critique_details=critique_details.dict(),
                overall_score=overall_score,
                timestamp=datetime.now()
            )
        except Exception as e:
            logging.error(f"Error in critique_artwork: {str(e)}")
            raise
                 
    async def describe_image(self, test_artwork_dict: Dict) -> str:
        """Describe the content of the image"""
        critique_prompt = f"""describe the content of the image in detail, respond in json
        """
        messages = self._add_image_to_message(critique_prompt, test_artwork_dict['drawing'])
        result = await self.critic_agent.a_generate_reply(messages, sender=self.user_proxy)
        return result

def create_critic_agent(agent_profile: Dict) -> CreativeArtCritic:
    """Factory function to create a critic agent from an agent profile"""
    return CreativeArtCritic(
        art_values=agent_profile.get('art_values', {}),
        name=f"Critic_{agent_profile.get('name', 'Anonymous')}"
    ) 
    
if __name__ == "__main__":
    import asyncio
    import yaml
    from PIL import Image

    artwork_dict = {
        'name': 'The Visionary Monkey', 
        'description': 'A post-impressionist fusion of digital art and classical romanticism, this artwork captures a cartoon-style monkey, embodying both modern pop culture and timeless artistic expression. The monkey, facing towards the right, wears a blue helmet adorned with white stars and red stripes, symbolizing Americana. With a calm demeanor, it smokes a pipe, exuding old-world charm amidst a vibrant teal and red color palette. The piece reflects a blend of simplicity and depth, bridging digital trends with a poetic, nostalgic essence.', 
        'image_url': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-RtsbKZPvXFWdJXwHx43FCbEY/user-LQ4IvvLkYFv3RmBmkvWqbdL5/img-B8K9qLRqDhlKZfNHulQXeYR1.png?st=2024-12-14T20%3A33%3A36Z&se=2024-12-14T22%3A33%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-12-14T05%3A09%3A34Z&ske=2024-12-15T05%3A09%3A34Z&sks=b&skv=2024-08-04&sig=RjFtEsZ2azwHvvJH/%2BSB/wNsjRTEZ5KV7ZHVD9p%2Bn3c%3D',
        'local_image_path': 'images/artwork_9345feb3-efa8-4e0c-a3d1-3135ddac49ac.png', 
        'art_style': 'Post-Impressionism with Romanticism Classical Poetry', 
        'attributes': {'Character': 'Cartoon-style monkey with a calm demeanor', 
                       'Accessories': 'Blue helmet with white stars and red stripes, smoking a pipe', 
                       'Color Palette': 'Bold and vibrant with teal background, red shirt, and blue helmet', 
                       'Expression': 'Laid-back and relaxed', 
                       'Theme': 'Blend of pop culture, Americana, and digital art trends', 
                       'Mood': 'Relaxed, casual, with a hint of nostalgia', 
                       'Unique Features': 'American flag motif helmet, pipe smoking', 
                       'Orientation': 'Main character faces towards the right'}, 
        'background_story': "In the digital realm where dreams take flight,  \nA cartoon monkey stands, a curious sight.  \nWith eyes serene and a calm, laid-back grace,  \nHe wears a helmet, stars and stripes in place.  \n\nA nod to Americana, bold and bright,  \nHis helmet gleams in the virtual light.  \nA pipe he smokes, with tendrils rising high,  \nA touch of old-world charm beneath the sky.  \n\nIn vibrant hues of teal and red, he stands,  \nA figure drawn by unseen artist's hands.  \nThe lines are clean, the colors bold and true,  \nA simple form, yet rich in meaning too.  \n\nThis monkey, calm amidst the digital storm,  \nEmbodies trends where pop and culture swarm.  \nA symbol of the times, both new and old,  \nIn NFT's embrace, his story's told.  \n\nA relic of nostalgia, yet so new,  \nHe bridges worlds, a vision to pursue.  \nIn every pixel, echoes of the past,  \nA timeless charm, in digital art cast.  \n\nSo here he stands, a character unique,  \nIn vibrant realms where art and tech do speak.  \nA testament to creativity's flight,  \nThis monkey shines, a beacon in the night.  ",
        'creation_context': "**NFT Analysis**\n\n1. **Key Visual Elements and Traits:**\n   - **Character:** The central figure is a cartoon-style monkey, which is a common motif in NFT art, especially in popular collections like the Bored Ape Yacht Club.\n   - **Accessories:** The monkey is wearing a blue helmet with white stars and red stripes, resembling an American flag, which adds a patriotic or Americana theme to the piece.\n   - **Expression:** The monkey has a calm demeanor, adding a laid-back or relaxed vibe to the character.\n   - **Additional Details:** The monkey is smoking a pipe, with smoke visibly rising, which contributes to its distinctive personality.\n\n2. **Color Schemes and Artistic Style:**\n   - **Color Palette:** The image uses a bold and vibrant color scheme. The teal background contrasts with the red shirt and the blue helmet, making the monkey the focal point.\n   - **Artistic Style:** The illustration is cartoonish, with clean lines and flat colors, typical of many digital art and NFT styles. The simplicity in design allows for easy recognition and reproduction in a series.\n\n3. **Unique or Distinctive Features:**\n   - **Helmet Design:** The helmet's American flag motif is a unique feature that may symbolize themes of patriotism or cultural references.\n   - **Pipe Smoking:** The inclusion of a pipe adds an element of sophistication or old-world charm, setting it apart from other similar NFT characters.\n\n4. **Overall Theme and Mood:**\n   - **Theme:** The image blends elements of pop culture, Americana, and digital art trends, likely appealing to collectors interested in these themes.\n   - **Mood:** The mood is relaxed and casual, with a hint of nostalgia due to the pipe and the retro-style helmet design.\n\nThis NFT likely belongs to a collection that emphasizes personality and cultural references, using a recognizable character in various thematic settings. The combination of a distinct character design with cultural motifs makes it appealing to a wide audience, particularly those interested in digital art and collectibles.", 'analysis': "**NFT Analysis**\n\n1. **Key Visual Elements and Traits:**\n   - **Character:** The central figure is a cartoon-style monkey, which is a common motif in NFT art, especially in popular collections like the Bored Ape Yacht Club.\n   - **Accessories:** The monkey is wearing a blue helmet with white stars and red stripes, resembling an American flag, which adds a patriotic or Americana theme to the piece.\n   - **Expression:** The monkey has a calm demeanor, adding a laid-back or relaxed vibe to the character.\n   - **Additional Details:** The monkey is smoking a pipe, with smoke visibly rising, which contributes to its distinctive personality.\n\n2. **Color Schemes and Artistic Style:**\n   - **Color Palette:** The image uses a bold and vibrant color scheme. The teal background contrasts with the red shirt and the blue helmet, making the monkey the focal point.\n   - **Artistic Style:** The illustration is cartoonish, with clean lines and flat colors, typical of many digital art and NFT styles. The simplicity in design allows for easy recognition and reproduction in a series.\n\n3. **Unique or Distinctive Features:**\n   - **Helmet Design:** The helmet's American flag motif is a unique feature that may symbolize themes of patriotism or cultural references.\n   - **Pipe Smoking:** The inclusion of a pipe adds an element of sophistication or old-world charm, setting it apart from other similar NFT characters.\n\n4. **Overall Theme and Mood:**\n   - **Theme:** The image blends elements of pop culture, Americana, and digital art trends, likely appealing to collectors interested in these themes.\n   - **Mood:** The mood is relaxed and casual, with a hint of nostalgia due to the pipe and the retro-style helmet design.\n\nThis NFT likely belongs to a collection that emphasizes personality and cultural references, using a recognizable character in various thematic settings. The combination of a distinct character design with cultural motifs makes it appealing to a wide audience, particularly those interested in digital art and collectibles.", 'poem': "In the digital realm where dreams take flight,  \nA cartoon monkey stands, a curious sight.  \nWith eyes serene and a calm, laid-back grace,  \nHe wears a helmet, stars and stripes in place.  \n\nA nod to Americana, bold and bright,  \nHis helmet gleams in the virtual light.  \nA pipe he smokes, with tendrils rising high,  \nA touch of old-world charm beneath the sky.  \n\nIn vibrant hues of teal and red, he stands,  \nA figure drawn by unseen artist's hands.  \nThe lines are clean, the colors bold and true,  \nA simple form, yet rich in meaning too.  \n\nThis monkey, calm amidst the digital storm,  \nEmbodies trends where pop and culture swarm.  \nA symbol of the times, both new and old,  \nIn NFT's embrace, his story's told.  \n\nA relic of nostalgia, yet so new,  \nHe bridges worlds, a vision to pursue.  \nIn every pixel, echoes of the past,  \nA timeless charm, in digital art cast.  \n\nSo here he stands, a character unique,  \nIn vibrant realms where art and tech do speak.  \nA testament to creativity's flight,  \nThis monkey shines, a beacon in the night.  ", 
        'uuid': '9345feb3-efa8-4e0c-a3d1-3135ddac49ac'}
    

    # Test the critic
    async def test_critic():
        character_profile = yaml.safe_load(open('teleAgent/characters/VincentVanGogh.yaml'))
        character_profile['art_values']={
            'personality': character_profile['personality'],
            'art_preference': character_profile['art_preference'],
            'art_dislike': character_profile['art_dislike']
        }
        critic = create_critic_agent(character_profile)
        
        # Create a test artwork dict
        test_artwork = {
            'name': 'Test Artwork',
            'description': 'A test artwork for the critic',
            'art_style': '-',
            'poem': 'A test poem',
            'drawing': './images/artwork_234d95c4-45ef-4ed4-9038-c6531367afca.png'
        }
        
        result = await critic.critique_artwork(test_artwork)
        print(result)

    asyncio.run(test_critic())
    
    