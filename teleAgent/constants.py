from datetime import datetime
from enum import Enum, auto
from pathlib import Path


class InteractionScene(str, Enum):
    """Enumeration of possible interaction scenes between users and agents"""

    TWITTER_REPLY = "twitter_reply"  # Twitter reply interactions
    TWITTER_SEND_TWEET = "twitter_send_tweet"  # Twitter send tweet
    TELEGRAM_PRIVATE = "telegram_private"  # Telegram private chats
    TELEGRAM_GROUP = "telegram_group"  # Telegram group chats

    @classmethod
    def is_twitter(cls, scene: str) -> bool:
        """Check if scene is Twitter-related"""
        return scene in [
            cls.TWITTER_REPLY.value,
        ]

    @classmethod
    def is_telegram(cls, scene: str) -> bool:
        """Check if scene is Telegram-related"""
        return scene in [cls.TELEGRAM_PRIVATE.value, cls.TELEGRAM_GROUP.value]

    @classmethod
    def is_public(cls, scene: str) -> bool:
        """Check if scene is public interaction"""
        return scene in [
            cls.TWITTER_REPLY.value,
            cls.TELEGRAM_GROUP.value,
        ]


RECORD_DIR='data_record'
TIMESTAMP_FORMAT = '%Y-%m-%d_%H:%M:%S'
THIS_MOMENT = datetime.strftime(datetime.now(), TIMESTAMP_FORMAT)
DATA_STORE_ROOT = Path(f'{RECORD_DIR}/{THIS_MOMENT}')

GROUP_CHAT_INTERVAL = 30 # seconds
ARTWORK_CREATION_INTERVAL = 10  # seconds

IMAGE_FILE_NAME_FORMAT = "artwork_{uuid}.png"

POS_EMO_PRICE_FACTOR = 0.00002
NEG_EMO_PRICE_FACTOR = -0.00001
CRITIQUE_PRICE_FACTOR = 0.0001

DRAWING_PROBABILITY = 0.0
MARKET_ADJUSTMENT_PROBABILITY = 0.0

ARTWORK_CREATION_TEMPLATE = "Hi everyone, I just created an NFT artwork titled #{name}#. It describes {description}. Any comments?"
DEAL_MADE_TEMPLATE = "🤝 Deal made! {buyer_name} has purchased the artwork from {seller_name} for {price:.2f} tokens!"
