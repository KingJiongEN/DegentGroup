import aiohttp
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from injector import inject

from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.models.twitter_auth import TwitterAuthModel
from .twitter_auth_service import TwitterAuthService
import logging
class TwitterAgentService:
    @inject
    def __init__(self, twitter_auth_dao: ITwitterAuthDAO, twitter_auth_service: TwitterAuthService):
        self.twitter_auth_dao = twitter_auth_dao
        self.twitter_auth_service = twitter_auth_service
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def post_tweet(self, auth_id: str, tweet_text: str) -> Optional[dict]:
        self.logger.info(f"Posting tweet: {tweet_text}")
        auth = await self.twitter_auth_service.refresh_token(auth_id)
        if not auth:
            self.logger.error("Failed to refresh token")
            return None

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://api.twitter.com/2/tweets",
                    headers={
                        "Authorization": f"Bearer {auth.access_token}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "text": tweet_text
                    },
            ) as resp:
                if resp.status != 201:
                    error_message = await resp.text()
                    self.logger.error(f"Error: Received status code {resp.status}, Details: {error_message}")
                    return None
                self.logger.info("Tweet posted successfully")
                return await resp.json()

    async def reply_to_tweet(self, auth_id: str, tweet_text: str, tweet_id: str) -> Optional[dict]:
        self.logger.info(f"Replying to tweet {tweet_id} with text: {tweet_text}")
        auth = await self.twitter_auth_service.refresh_token(auth_id)
        if not auth:
            self.logger.error("Failed to refresh token")
            return None

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://api.twitter.com/2/tweets",
                    headers={
                        "Authorization": f"Bearer {auth.access_token}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "text": tweet_text,
                        "reply": {
                            "in_reply_to_tweet_id": tweet_id
                        }
                    },
            ) as resp:
                if resp.status != 201:
                    error_message = await resp.text()
                    self.logger.error(f"Error: Received status code {resp.status}, Details: {error_message}")
                    return None
                self.logger.info("Reply posted successfully")
                return await resp.json()

    async def read_tweet(self, auth_id: str, tweet_id: str) -> Optional[dict]:
        self.logger.info(f"Reading tweet {tweet_id}")
        auth = await self.twitter_auth_service.refresh_token(auth_id)
        if not auth:
            self.logger.error("Failed to refresh token")
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.twitter.com/2/tweets/{tweet_id}",
                    headers={
                        "Authorization": f"Bearer {auth.access_token}",
                    },
            ) as resp:
                if resp.status != 200:
                    error_message = await resp.text()
                    self.logger.error(f"Error: Received status code {resp.status}, Details: {error_message}")
                    return None
                self.logger.info("Tweet read successfully")
                return await resp.json()