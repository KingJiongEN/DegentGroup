from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class MemoryType(Enum):
    """Types of memories an agent can have"""

    DIALOG = "dialog"  # Conversation memory
    EMOTION = "emotion"  # Emotional response memory
    INTERACTION = "interaction"  # User interaction memory
    EVENT = "event"  # Special event memory


@dataclass
class Memory:
    """Represents a single memory entry for an agent"""

    id: str
    agent_id: str
    user_id: str
    content: str
    memory_type: MemoryType
    created_at: datetime
    expires_at: datetime
    context: Dict[str, Any] = None  # Additional context data
    emotion_score: float = 0.0  # Emotional impact score
    importance: int = 1  # Memory importance (1-10)

    def is_expired(self) -> bool:
        """Check if memory has expired"""
        return datetime.now() > self.expires_at

    def time_until_expiry(self) -> float:
        """Get hours remaining until memory expires"""
        if self.is_expired():
            return 0
        delta = self.expires_at - datetime.now()
        return delta.total_seconds() / 3600
