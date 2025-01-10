from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Optional


class SenderType(Enum):
    USER = "user"
    AGENT = "assistant"

class DialogType(Enum):
    MESSAGE = "message"
    COMMAND = "command"

@dataclass
class Dialog:
    """对话模型类"""

    id: str
    user_id: str
    agent_id: str
    sender: Literal["user", "assistant"]
    content: str
    type: Literal["message", "command"]
    platform: str
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def is_command(self) -> bool:
        """判断是否是命令类型消息"""
        return self.type == DialogType.COMMAND

    def get_platform_formatted_content(self) -> str:
        """根据不同平台格式化内容"""
        if self.platform == "twitter":
            # Twitter 限制280字符
            return self.content[:280]
        elif self.platform == "telegram":
            # Telegram 限制4096字符
            return self.content[:4096]
        return self.content

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "sender": self.sender,
            "content": self.content,
            "type": self.type,
            "platform": self.platform,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
