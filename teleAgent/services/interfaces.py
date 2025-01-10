from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update

from teleAgent.models.agent import Agent
from teleAgent.models.dialog import Dialog
from teleAgent.models.memory import Memory
from teleAgent.models.nft import NFT
from teleAgent.models.wallet import Balance
from teleAgent.models.twitter_auth import TwitterAuthModel

class IAgentService(ABC):
    @abstractmethod
    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """Retrieve an agent by ID"""
        pass

    @abstractmethod
    async def get_agent_for_chat(self, chat_id: int) -> Agent:
        """Get or create agent for a specific chat"""
        pass

    @abstractmethod
    async def process_message(
        self, agent_id: str, user_id: str, is_bot: bool, content: str, scene: str
    ) -> str:
        """Process incoming message and generate response based on agent personality"""
        pass

    @abstractmethod
    async def get_response(self, bot_id: int, update: Update, message: str) -> str:
        """Get agent's response to a message"""
        pass

    @abstractmethod
    async def cleanup_expired_memory(self, agent_id: str) -> int:
        """Clean up expired memories"""
        pass


class IWalletService(ABC):
    @abstractmethod
    async def get_balance(self, wallet_address: str) -> Balance:
        """Get wallet balance"""
        pass

    @abstractmethod
    async def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer tokens between wallets"""
        pass

    @abstractmethod
    async def create_wallet(self) -> str:
        """Create new wallet and return address"""
        pass


class INFTService(ABC):
    @abstractmethod
    async def get_latest_mints(self, limit: int = 5) -> List[NFT]:
        """Get most recently minted NFTs"""
        pass

    @abstractmethod
    async def get_agent_nfts(self, agent_id: str) -> List[NFT]:
        """Get NFTs owned by an agent"""
        pass

    @abstractmethod
    async def mint(self, creator_id: str, metadata: Dict) -> NFT:
        """Mint new NFT"""
        pass

    @abstractmethod
    async def transfer_nft(self, nft_id: str, from_id: str, to_id: str) -> bool:
        """Transfer NFT ownership"""
        pass


class IMemoryService(ABC):
    @abstractmethod
    async def add_memory(self, agent_id: str, user_id: str, content: str) -> Memory:
        """Add new memory"""
        pass

    @abstractmethod
    async def get_recent_memories(
        self, agent_id: str, user_id: str, hours: int = 24
    ) -> List[Memory]:
        """Get recent memories within time window"""
        pass

    @abstractmethod
    async def clear_old_memories(self, hours: int = 24) -> int:
        """Clear memories older than specified hours"""
        pass


class IDialogService(ABC):
    @abstractmethod
    async def create_dialog(self, agent_id: str, user_id: str) -> Dialog:
        """Create new dialog session"""
        pass

    @abstractmethod
    async def get_dialog(self, dialog_id: str) -> Optional[Dialog]:
        """Get dialog by ID"""
        pass

    @abstractmethod
    async def add_message(self, dialog_id: str, content: str, is_agent: bool) -> None:
        """Add message to dialog"""
        pass

class ITwitterAuthService(ABC):
    @abstractmethod
    async def create_oauth_url(self, agent_id: str) -> str:
        """Create Twitter OAuth URL for agent"""
        pass

    @abstractmethod
    async def handle_callback(
            self, agent_id: str, code: str, state: str, code_verifier: str
    ) -> Optional[TwitterAuthModel]:
        """Handle OAuth callback"""
        pass

    @abstractmethod
    async def refresh_token(self, auth_id: str) -> Optional[TwitterAuthModel]:
        """Refresh Twitter access token"""
        pass
