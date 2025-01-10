import base64
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import os
import random
import uuid
from typing import Dict, List, Optional, Union
from telegram import Update
import yaml
from pathlib import Path
from PIL import Image
from io import BytesIO
from autogen import SwarmAgent

from sqlalchemy.orm import sessionmaker

from teleAgent.daos.agent.impl import AgentDAO
from teleAgent.daos.agent.interface import IAgentDAO
from teleAgent.daos.dialog.impl import DialogDAO
from teleAgent.daos.nft.impl import NFTDAO
from teleAgent.models.agent import Agent
from teleAgent.models.agent_model.artwork_creation.artwork_creater import create_artwork_agent
from teleAgent.models.agent_model.bargain.bargainer import create_bargain_group_chat, single_round_response
from teleAgent.models.agent_model.proact_groupagent import ProactGroupAgent
from teleAgent.models.agent_model.simutan_group import SimutanGroup, MyGroupManager
from teleAgent.models.agent_model.utilities.small_tools import convert_pil_to_bytes, get_base64_image
from teleAgent.models.market.artificial_market import ArtificialMarket
from teleAgent.services.interfaces import IAgentService
from teleAgent.constants import ARTWORK_CREATION_TEMPLATE, DEAL_MADE_TEMPLATE, InteractionScene
from teleAgent.models.agent_model.constant.llm_configs import llm_config_gpt4o, llm_config_gpt4o_unstructured
from teleAgent.core.config import settings

from teleAgent.integrations.telegram import TelegramResponse
from teleAgent.daos.nft.interface import INFTDAO
from teleAgent.daos.artwork_critique.interface import IArtworkCritiqueDAO
from teleAgent.models.nft import NFT, NFTMetadata, NFTStatus
from teleAgent.models.agent_model.artwork_creation.artwork_critic import ArtworkCritiqueBase, create_critic_agent
from teleAgent.daos.artwork_critique.impl import ArtworkCritiqueDAO
from teleAgent.models.artwork_critique import ArtworkCritique
from teleAgent.models.dialog import Dialog, DialogType, SenderType
import uuid

@dataclass
class MultiResponse:
    """Class to handle multiple responses"""
    messages: List[str]
    RESPONSE_SPLITTERS = ['. ', '! ', '? ']  # Add all possible splitters here

    @classmethod
    def from_text(cls, text: str) -> 'MultiResponse':
        """Create a MultiResponse by splitting text on all defined splitters"""
        # Initialize with the full text
        messages = [text]
        
        # Iteratively split by each splitter
        for splitter in cls.RESPONSE_SPLITTERS:
            # Split each existing message and flatten the result
            new_messages = []
            for msg in messages:
                # Keep the splitter with each segment except the last one
                segments = msg.split(splitter)
                split = []
                for i, segment in enumerate(segments):
                    if segment.strip():  # Only include non-empty segments
                        if i < len(segments) - 1:  # Add splitter back to all but last segment
                            split.append(segment.strip() + splitter)
                        else:  # Last segment doesn't get a splitter unless it had one in original text
                            split.append(segment.strip())
                new_messages.extend(split)
            messages = new_messages
            
        return cls(messages=messages)

    def to_telegram_responses(self) -> List[TelegramResponse]:
        """Convert to list of TelegramResponses"""
        return [TelegramResponse.text_response(msg) for msg in self.messages]

class AgentService(IAgentService):

    def __init__(
        self,
        session_factory: sessionmaker,
        nft_dao: INFTDAO,
        artwork_critique_dao: IArtworkCritiqueDAO,
        agent_dao: IAgentDAO
    ):
        self._agents: Dict[str, Agent] = {}
        self._chat_agents: Dict[int, Agent] = {}
        self._memories: Dict[
            str, Dict[str, list]
        ] = defaultdict(lambda: defaultdict(list))  # agent_id -> {user_id: [memories]}
        self.dialog_dao = DialogDAO(session_factory)
        self.nft_dao = nft_dao
        self.artwork_critique_dao = artwork_critique_dao
        self.agent_dao = agent_dao
        # Pre-populate with test agents
        self._create_agents()
        self.artificial_market = ArtificialMarket(session_factory, artwork_critique_dao, nft_dao, agent_dao)
        
    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """Retrieve an agent by ID"""
        if isinstance(agent_id, int):
            agent_id = str(agent_id)
        return self._agents.get(agent_id)

    async def get_agent_for_chat(self, chat_id: int) -> Agent:
        """Get or create agent for a specific chat
        Deprecated
        """
        raise NotImplementedError("This method is deprecated and should not be used.")
        if chat_id not in self._chat_agents:
            # Assign random test agent
            import random

            agent = random.choice(list(self._agents.values()))
            self._chat_agents[chat_id] = agent
        return self._chat_agents[chat_id]

    async def process_message(
        self, agent_id: str, user_id: str, is_bot: bool, content: str, scene: str
    ) -> Union[TelegramResponse, MultiResponse]:
        """Process incoming message and generate response based on agent personality"""
        # Convert IDs to strings if they aren't already
        agent_id = str(agent_id)
        user_id = str(user_id)
        
        agent:ProactGroupAgent = self.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")

        if InteractionScene.is_telegram(scene):
            
            if scene == InteractionScene.TELEGRAM_PRIVATE:
                self.store_message_to_db(agent_id, user_id, content, scene, SenderType.USER)                

                messages = self.build_telegram_private_message_history_from_db(user_id, agent_id)

                bargain_agent_ls:List[SwarmAgent] = self.build_recipient_agent(user_id, agent, scene, messages)

                chat_result = await single_round_response(bargain_agent_ls, 
                                                          {"character_profile": agent.PROFILE_MESSAGE.format(self=agent), "wallet_address": agent.wallet_address},
                                                        messages)
                response = chat_result.response 
                
                self.store_message_to_db(agent_id, user_id, response, scene, SenderType.AGENT)
                
                if any(splitter in response for splitter in MultiResponse.RESPONSE_SPLITTERS):
                    return MultiResponse.from_text(response) 
                return TelegramResponse.text_response(response)

            if scene == InteractionScene.TELEGRAM_GROUP:
                response = await agent.a_generate_group_chat_response()
                await self.store_TGgroup_message(agent, response, scene)
                
                # Check if response contains any splitter
                if any(splitter in response for splitter in MultiResponse.RESPONSE_SPLITTERS):
                    return MultiResponse.from_text(response)
                return TelegramResponse.text_response(response)
            
        elif InteractionScene.is_twitter(scene):
            return await self.handle_twitter_message(agent, user_id, content)

        raise ValueError(f"Unsupported interaction scene: {scene}")
        


    async def get_response(self, bot_id: int, update: Update, message: str) -> TelegramResponse:
        scene = (
            InteractionScene.TELEGRAM_GROUP 
            if update.effective_chat.type in ['group', 'supergroup'] 
            else InteractionScene.TELEGRAM_PRIVATE
        )
        is_bot = update.effective_user.is_bot
        assert bot_id == settings.TELEGRAM_BOT_ID, "Bot ID does not match"
        
        # Convert IDs to strings
        agent_id = str(bot_id)
        user_id = str(update.effective_chat.id)
        
        if not agent_id:
            error_msg = f"No agent configured for Telegram bot ID: {bot_id}"
            logging.error(error_msg)
            raise ValueError(error_msg)

        try:
            return await self.process_message(
                agent_id=agent_id,
                user_id=user_id,
                is_bot=is_bot,
                content=message,
                scene=scene
            )
        except Exception as e:
            error_msg = f"Error processing message for bot {bot_id}: {str(e)}"
            logging.error(error_msg, exc_info=True)
            return "I'm sorry, I encountered an error processing your message. Please try again later."

    async def cleanup_expired_memory(self, agent_id: str) -> int:
        """Clean up expired memories"""
        if agent_id not in self._memories:
            return 0

        cleaned = 0
        cutoff = datetime.now() - timedelta(hours=24)

        for user_id in self._memories[agent_id]:
            original_len = len(self._memories[agent_id][user_id])
            self._memories[agent_id][user_id] = [
                m for m in self._memories[agent_id][user_id] if m["timestamp"] > cutoff
            ]
            cleaned += original_len - len(self._memories[agent_id][user_id])

        return cleaned

    def cleanup_user_memory_from_db(self, agent_id: str, user_id: str):
        deleted_count = self.dialog_dao.delete_by_user_and_agent(user_id=user_id, agent_id=agent_id)
        return deleted_count
        
    def build_recipient_agent(self, user_id: str, agent: ProactGroupAgent, scene: str, messages: List[Dict]) -> List[SwarmAgent]:
        bargain_agent_ls = create_bargain_group_chat(
            agent_id=agent.id,
            nft_dao=self.nft_dao, 
            artwork_critique_dao=self.artwork_critique_dao, 
            agent_inner_state=agent.inner_states
        )
        
        return bargain_agent_ls
        
    def build_telegram_private_message_history(self, user_id: str, agent_id: str) -> List[Dict]:
        memories = self._memories.get(agent_id, {}).get(user_id, [])
        messages = []
        for memory in memories:
            messages.append({"role": memory.get("role"), "content": memory.get("content")})
        return messages
    
    def build_telegram_private_message_history_from_db(self, user_id: str, agent_id: str) -> List[Dict]:
        messages = self.dialog_dao.get_by_user_and_agent(user_id, agent_id)
        # format messages to the format of OpenAI ChatCompletion
        formatted_messages = []
        for message in messages:
            formatted_messages.append({"role": message.sender, "content": message.content, 'name': 'user' if message.sender == SenderType.USER.value else 'Bargainer' })
        formatted_messages.reverse()
        return formatted_messages
    
    async def store_TGgroup_message(self, agent:ProactGroupAgent, content:str, scene:str, role:str=None):
        # TODO: store in to db or just store part of the message to save memory
        await agent.update_groupchat(content, role)
    
    async def act_periodically_artwork_creation(self, agent: ProactGroupAgent) -> TelegramResponse:
       
        async def art_creation(agent: ProactGroupAgent) -> dict:
            art_agent = create_artwork_agent(agent.art_values, agent.wallet_address,agent.id)
            art_work_dict = await art_agent.create_complete_artwork(agent.groupchat.messages)
             # Convert PIL Image to bytes
            if isinstance(art_work_dict['drawing'], Image.Image):
                art_work_dict['drawing_base64'] = convert_pil_to_bytes(art_work_dict['drawing'])
            else:
                raise ValueError("Expected PIL Image object")
            return art_work_dict
        
        try:
            art_work_dict = await art_creation(agent)
            nft = await self.store_nft2db(art_work_dict['token_id'], art_work_dict['nft_metadata'], agent)
            art_work_dict['nft_id'] = nft.token_id
            
            critics:List[ArtworkCritique] = await self.critic_artwork(agent, art_work_dict)
            
            await self.store_artwork_critic(agent, art_work_dict, critics)
            
            text = ARTWORK_CREATION_TEMPLATE.format(name=art_work_dict["name"], description=art_work_dict["description"])
            await self.store_TGgroup_message(agent, text, InteractionScene.TELEGRAM_GROUP)
             
            return TelegramResponse.media_with_text(
                text=text,
                caption=f'{art_work_dict["name"]}',
                image=art_work_dict['drawing_base64']
            )
        except Exception as e:
            logging.error(f"Error in act_periodically_artwork_creation: {str(e)}")
            return TelegramResponse.text_response(
                "Sorry, I encountered an error while creating artwork. Let's continue our conversation."
            )
    
    async def act_periodically_market_adjust(self, agent: ProactGroupAgent) -> TelegramResponse:
        deal = await self.artificial_market.agent_sell(agent.id, self._get_agents_inner_states())
        return deal
        if deal:
            nft_id = deal['nft_id']
            buyer_name = self._agents[deal['buyer_id']].name_str
            seller_name = self._agents[deal['seller_id']].name_str
            amount = deal['transaction_amount']
            nft_image_path = self.nft_dao.get_by_token_id(nft_id).metadata.image_url
            nft_name = self.nft_dao.get_by_token_id(nft_id).metadata.name
            
            # load and resize image
            image = Image.open(nft_image_path)
            assert isinstance(image, Image.Image)
            img_byte_arr = convert_pil_to_bytes(image)
            
            return TelegramResponse.media_with_text(
                text=DEAL_MADE_TEMPLATE.format(buyer_name=buyer_name, amount=amount),
                image=img_byte_arr,
                caption=f"{nft_name}"
            )
        
    
    async def critic_artwork(self, agent: ProactGroupAgent, artwork_dict: dict) -> List[ArtworkCritique]:
        """Generate critiques from other agents about the artwork"""
        critics = []
        
        # Get all agents except the creator
        critic_agents = [self.get_by_id(a.id) for a in self.agent_dao.list_active()] # FIXME: use db instead of in-memory
        
        for critic_agent in critic_agents:
            try:
                # Create a critic agent for each agent based on their profile
                art_critic = create_critic_agent({'art_values': critic_agent.art_values,
                                                  'name': critic_agent.name_str})
                
                # Generate critique
                critique_result: ArtworkCritiqueBase = await art_critic.critique_artwork(artwork_dict)
                
                critics.append(ArtworkCritique(
                    id=str(uuid.uuid4()),
                    nft_id=artwork_dict['token_id'],
                    critic_agent_id=critic_agent.id,
                    critic_agent_name=critic_agent.name_str,
                    critique_details=critique_result.critique_details,
                    overall_score=critique_result.overall_score,
                    created_at=critique_result.timestamp
                ))
                
            except Exception as e:
                logging.error(f"Error getting critique from agent {critic_agent.id}: {str(e)}")
                continue
                
        return critics
   
    def store_message(self, agent_id: str, user_id: str, content: str, scene: str, sender: str):
        self._memories[agent_id][user_id].append(
            {"content": content, "role": sender, "timestamp": datetime.now(), "scene": scene}
        )
        
    def store_message_to_db(self, agent_id: str, user_id: str, content: str, scene: str, sender: SenderType):
        content = self._truncate_content(content)
        self.dialog_dao.create(Dialog(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            user_id=user_id,
            sender=sender.value,
            content=content,
            type=DialogType.MESSAGE.value,
            created_at=datetime.now(),
            platform=scene
        ))

    def _truncate_content(self, content: str, max_length: int = 1000) -> str:
        """Truncate content to fit database column size with ellipsis."""
        if len(content) > max_length:
            return content[:max_length-3] + "..."
        return content
    
    def _create_agents(self):
        """Create test agents"""
        agents_ls: List[ProactGroupAgent] = []
        character_yml_ls = os.listdir('teleAgent/characters')
        for yml in character_yml_ls:
            if not yml.endswith('.yaml'): continue
            char_cfg = yaml.safe_load(open(f'teleAgent/characters/{yml}'))
            char_cfg['llm_config']=llm_config_gpt4o_unstructured
            agents_ls.append(ProactGroupAgent(**char_cfg))
        

        for agent in agents_ls:
            self._agents[agent.id] = agent
       
        self._store_agents_to_db()
        
        topic = os.environ.get('TOPIC', 'BAYC')
        topic_content = yaml.safe_load(open(f'teleAgent/topics/{topic}.yaml'))['content']
        image_folder = yaml.safe_load(open(f'teleAgent/topics/{topic}.yaml'))['image_folder']
        
        # Add error handling for image loading
        try:
            image_ls = list(Path(image_folder).glob('*.png'))
            if not image_ls:
                logging.warning(f"No PNG images found in folder: {image_folder}")
                random_images = []
            else:
                random.seed(42)
                random_images = random.sample(image_ls, k=min(2, len(image_ls)))
        except Exception as e:
            logging.error(f"Error loading images from {image_folder}: {str(e)}")
            random_images = []
        
         
        def create_welcome_message(random_images:List[Path]):
            return_ls = [
                {
                    "type": "text",
                    "text": f"Hello, welcome to the art salon. Today's topic is {topic}. "
                },
            ]
            
            if random_images:
                for image_path in random_images:
                    try:
                        base64_image = get_base64_image(str(image_path))
                        return_ls.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        })
                    except Exception as e:
                        logging.error(f"Error processing image {image_path}: {str(e)}")
            
            return return_ls
        
        self.group_chat = SimutanGroup(
            agents=agents_ls,
            messages=[
                {'name': "VincentVanGogh", 
                'content': create_welcome_message(random_images)
                } 
            ],
            resource=f'''
            This is an art salon. Today's topic is {topic}
            {topic_content}
            '''
        )
        
    def _store_agents_to_db(self):
        telegram_bot_id = str(settings.TELEGRAM_BOT_ID)  # Ensure string conversion
        this_agent = self.get_by_id(telegram_bot_id)
        if this_agent and not self.agent_dao.get_by_id(telegram_bot_id):
            try:
                self.agent_dao.create(this_agent)
            except Exception as e:
                logging.error(f"Failed to create agent in database: {e}")
        elif not this_agent:
            logging.error(f"Agent not found: {telegram_bot_id}")
    
    def _get_agents_inner_states(self):
        return {agent.id: agent.inner_states for agent in self._agents.values()} # FIXME: use db instead of in-memory
    
    async def store_nft2db(self, token_id: str, metadata: NFTMetadata, agent: ProactGroupAgent) -> NFT:
        nft = NFT(
            id=token_id,  # Generate a new UUID
            token_id=token_id,  # Will be set when minted
            contract_address=token_id,  # Will be set when minted
            metadata=metadata,
            creator_id=agent.id,
            owner_id=agent.id,  # Initially owned by creator
            status=NFTStatus.DRAFT,
            created_at=datetime.now()
        )
        
        try:
            # Create and commit the NFT
            nft = self.nft_dao.create(nft)
            logging.info(f"NFT {nft.id} created and stored in database")
            return nft
            
        except Exception as e:
            logging.error(f"Failed to store NFT in database: {str(e)}")
            raise
    
    async def store_artwork_critic(self, agent: ProactGroupAgent, artwork_dict: dict, critics: List[ArtworkCritique]) -> NFT:
        """Store artwork as NFT and its critiques"""
        # First create the NFTMetadata object
        # metadata = NFTMetadata(
        #     name=artwork_dict["name"],
        #     description=artwork_dict["description"],
        #     image_url=artwork_dict["local_image_path"],
        #     art_style=artwork_dict["art_style"],
        #     attributes=artwork_dict["attributes"],
        #     background_story=artwork_dict["poem"],
        #     creation_context=artwork_dict["analysis"]
        # )
        
        
        # Create critiques
        for critic in critics:
            self.artwork_critique_dao.create(critic)
        