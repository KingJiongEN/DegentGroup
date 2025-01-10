from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class Agent:
    id: str
    name_str: str
    personality: str
    art_style: str
    profile: Optional[str] = None
    avatar: Optional[str] = None
    configs: Dict = None
    stats: Dict = None
    wallet_address: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        if self.configs is None:
            self.configs = {}
        if self.stats is None:
            self.stats = {}

    def register_tool(self, name: str, tool_fn: Callable) -> None:
        """Register a tool function that agent can use"""
        self.tools[name] = tool_fn

    def use_tool(self, name: str, *args, **kwargs) -> Any:
        """Execute a registered tool function"""
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name](*args, **kwargs)

    def generate_reply(self, message: str) -> str:
        # Business logic
        pass

    def publish_content(self) -> bool:
        # Business logic
        pass
