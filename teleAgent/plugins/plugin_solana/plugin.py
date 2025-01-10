from typing import Dict, Any
from dataclasses import dataclass

from teleAgent.models.agent import Agent
from .tools.check_balance import check_wallet_balance

@dataclass
class SolanaPluginConfig:
    """Solana Plugin Configuration"""
    rpc_url: str = "https://api.mainnet-beta.solana.com"
    network: str = "mainnet"
    auto_register: bool = True

class SolanaPlugin:
    """
    Solana Plugin
    Provides a set of tools related to the Solana blockchain
    """
    
    def __init__(self, config: SolanaPluginConfig = None):
        """
        Initialize the Solana Plugin
        
        Args:
            config: Plugin configuration, if None, default configuration is used
        """
        self.config = config or SolanaPluginConfig()
        self.tools = self._init_tools()
        
    def _init_tools(self) -> Dict[str, Any]:
        """Initialize all tool functions"""
        return {
            "check_balance": lambda address: check_wallet_balance(
                wallet_address=address,
                rpc_url=self.config.rpc_url
            ),
            # Add more tools here...
        }
    
    def register(self, agent: Agent) -> None:
        """
        Register all tools to the Agent
        
        Args:
            agent: The Agent instance to register tools to
        """
        for tool_name, tool_fn in self.tools.items():
            agent.register_tool(tool_name, tool_fn)
            
    @property
    def name(self) -> str:
        """Plugin name"""
        return "solana"
        
    @property
    def version(self) -> str:
        """Plugin version"""
        return "0.1.0"
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "network": self.config.network,
            "rpc_url": self.config.rpc_url,
            "tools": list(self.tools.keys())
        }

# Usage example
if __name__ == "__main__":
    # Create plugin instance
    config = SolanaPluginConfig(
        rpc_url="https://api.devnet.solana.com",
        network="devnet"
    )
    plugin = SolanaPlugin(config)
    
    # Create Agent instance
    agent = Agent(
        id="test_agent",
        name_str="TestAgent",
        personality="Helpful",
        art_style="Futurism",
        wallet_address="7KwpXpAKJS8x8NsX6EQxHYmWpyRjs9Qv7PhxqxcS5jV3"
    )
    
    # Register plugin tools
    plugin.register(agent)
    
    # Test tool usage
    try:
        balance = agent.use_tool("check_balance", agent.wallet_address)
        print(f"Wallet balance: {balance} SOL")
    except Exception as e:
        print(f"Error checking balance: {str(e)}")
    
    # Print plugin information
    print("\nPlugin info:")
    print(plugin.get_info())