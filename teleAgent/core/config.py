from typing import Any, Dict, List

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TraderAI"
    PROJECT_DESCRIPTION: str = "AI Agent Social Platform"
    VERSION: str = "0.1.0"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILES: List[str] = []
    LOG_CONSOLE: bool = True
    
    ALLOWED_HOSTS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = "postgresql://teleAgent:teleAgentsecret@localhost:5432/teleAgent"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Twitter API
    BASE_URL: str = "http://localhost:8000"
    TWITTER_API_KEY: str = "ajIyR2ZqZVNHN25mM2djeHRsd2M6MTpjaQ"
    TWITTER_API_SECRET: str = "0sDPPRjy2BVDrjwnqDcAR4i0_SSl3kZRtBuejOFS5ILeY51TpJ"

    # Telegram Bot
    TELEGRAM_BOT_ID: int = 7621063861
    TELEGRAM_TOKEN: str = "7621063861:AAF857glOx8mJBUzMj13SCI87Ze9jy2ws5g"
    TELEGRAM_USERNAME: str = "your_bot_username"
    TELEGRAM_TOOLS_TEST: bool = False

    # Solana
    SOLANA_RPC_URL: str = "https://api.mainnet-beta.solana.com"

    # OKEx API
    OKEX_API_KEY: str = "your_okex_api_key"
    OKEX_API_SECRET: str = "your_okex_api_secret"
    OKEX_PASSPHRASE: str = "your_okex_passphrase"
    OKEX_PROJECT_ID: str = "your_okex_project_id"  # Optional for WaaS endpoints
    OKEX_BASE_URL: str = "https://www.okx.com"

    # OpenAI
    OPENAI_API_KEY: str = "your_openai_key"

    # Arware
    ARWEAVE_NODE_HOST: str = "arweave.net"
    ARWEAVE_JWK_FILE: str = "your_arweave_jwk_file"
    ARWEAVE_ADDRESS: str = "your_arweave_address"
    
    # Token Metadata Service
    TOKEN_METADATA_SERVICE_URL: str = "http://localhost:3000"
    TOKEN_METADATA_SERVICE_TIMEOUT: int = 30
    NFT_PROGRAM_ID: str = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"

    # Solana & Metaplex
    METAPLEX_PRIVATE_KEY: str = "your_metaplex_private_key"
    METAPLEX_PUBLIC_KEY: str = "your_metaplex_public_key" 
    METAPLEX_DECRYPTION_KEY: str = "your_metaplex_decryption_key"
    MIN_SOL_BALANCE: int = 10000000

    model_config = ConfigDict(
        env_file=".env"
    )


settings = Settings()
