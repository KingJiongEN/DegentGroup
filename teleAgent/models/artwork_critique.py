from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class ArtworkCritique:
    """Represents a critique of an artwork"""
    
    id: str
    nft_id: str
    critic_agent_id: str
    critic_agent_name: str
    critique_details: Dict  # Detailed critique structure
    overall_score: float
    created_at: datetime 