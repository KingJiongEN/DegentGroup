from datetime import datetime, timedelta
from typing import Dict, Optional

from telegram import Update

from teleAgent.models.agent import Agent
from teleAgent.services.interfaces import IAgentService


class AgentServiceFake(IAgentService):
    def __init__(self):
        # Mock storage
        self._agents: Dict[str, Agent] = {}
        self._chat_agents: Dict[int, Agent] = {}
        self._memories: Dict[
            str, Dict[str, list]
        ] = {}  # agent_id -> {user_id: [memories]}

        # Pre-populate with test agents
        self._create_test_agents()

    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """Retrieve an agent by ID"""
        return self._agents.get(agent_id)

    async def get_agent_for_chat(self, chat_id: int) -> Agent:
        """Get or create agent for a specific chat"""
        if chat_id not in self._chat_agents:
            # Assign random test agent
            import random

            agent = random.choice(list(self._agents.values()))
            self._chat_agents[chat_id] = agent
        return self._chat_agents[chat_id]

    async def process_message(
        self, agent_id: str, user_id: str, content: str, scene: str
    ) -> str:
        """Process incoming message and generate response based on agent personality"""
        agent = self._agents.get(agent_id)
        if not agent:
            return "Agent not found"

        # Store in memory
        if agent_id not in self._memories:
            self._memories[agent_id] = {}
        if user_id not in self._memories[agent_id]:
            self._memories[agent_id][user_id] = []

        self._memories[agent_id][user_id].append(
            {"content": content, "timestamp": datetime.now(), "scene": scene}
        )

        # Mock response based on agent's personality
        return f"{agent.name_str} responds: Thanks for your message about {content}!"

    async def get_response(self, agent_id: str, update: Update, message: str) -> str:
        """Get agent's response to a message"""
        return await self.process_message(agent_id, update.effective_chat.id, message, "chat")

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

    def _create_test_agents(self):
        """Create test agents"""
        test_agents = [
            Agent(
                id="crypto_artist_1",
                name_str="CryptoArtist",
                personality="Creative and passionate about NFT art",
                art_style="Pop Art",
            ),
            Agent(
                id="trader_pro_1",
                name_str="TraderPro",
                personality="Analytical and market-focused",
                art_style="Surrealism",
            ),
            Agent(
                id="crypto_memer_1",
                name_str="CryptoMemer",
                personality="Humorous and meme-loving",
                art_style="Dadaism",
            ),
            Agent(
                id="tech_geek_1",
                name_str="TechGeek",
                personality="Technical and forward-thinking",
                art_style="Futurism",
            ),
        ]

        for agent in test_agents:
            self._agents[agent.id] = agent

    # Helper methods for testing
    async def _mock_reset(self):
        """Reset all data (for testing)"""
        self._agents.clear()
        self._chat_agents.clear()
        self._memories.clear()
        self._create_test_agents()
