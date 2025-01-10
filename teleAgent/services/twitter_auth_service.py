from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode
from uuid import uuid4

import aiohttp
from injector import inject

from teleAgent.core.config import settings
from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.models.twitter_auth import TwitterAuthModel
from .interfaces import ITwitterAuthService
import json
import base64
import hashlib
import secrets


class TwitterAuthService(ITwitterAuthService):
    @inject
    def __init__(self, twitter_auth_dao: ITwitterAuthDAO):
        self.twitter_auth_dao = twitter_auth_dao
        self.oauth_config = {
            "client_id": "ajIyR2ZqZVNHN25mM2djeHRsd2M6MTpjaQ",
            "client_secret": "0sDPPRjy2BVDrjwnqDcAR4i0_SSl3kZRtBuejOFS5ILeY51TpJ",
            "redirect_uri": "http://nh93eh.top/api/twitter/callback",
        }

    async def create_oauth_url(self, agent_id: str) -> str:
        code_verifier = secrets.token_urlsafe(64)[:128]
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('ascii')).digest()
        ).decode('ascii').rstrip('=')

        state = json.dumps({
            "agent_id": agent_id,
            "state": str(uuid4()),
            "code_verifier": code_verifier  # 存储 code_verifier
        })

        params = {
            "response_type": "code",
            "client_id": self.oauth_config["client_id"],
            "redirect_uri": self.oauth_config["redirect_uri"],
            "scope": "tweet.read users.read offline.access tweet.write",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",  # 使用 SHA-256
        }
        return f"https://twitter.com/i/oauth2/authorize?{urlencode(params)}"

    async def handle_callback(
            self, agent_id: str, code: str, state: str, code_verifier: str
    ) -> Optional[TwitterAuthModel]:
        # Verify state from storage
        # TODO: Implement state verification
        print(f"Received state: {state}")
        state_data = {
            "agent_id": agent_id,
            "state": state,
            "code_verifier": code_verifier
        }
        tokens = await self._exchange_code(code, state_data)
        if not tokens:
            return None

        # Delete existing auth if any
        await self.twitter_auth_dao.delete_by_agent_id(agent_id)

        # Create new auth record
        auth = TwitterAuthModel(
            id=str(uuid4()),
            agent_id=agent_id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_at=datetime.utcnow() + timedelta(seconds=tokens["expires_in"]),
        )

        return self.twitter_auth_dao.create(auth)

    async def refresh_token(self, auth_id: str) -> Optional[TwitterAuthModel]:
        auth = await self.twitter_auth_dao.get_by_id(auth_id)
        if not auth:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://api.twitter.com/2/oauth2/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": auth.refresh_token,
                        "client_id": self.oauth_config["client_id"],
                        "client_secret": self.oauth_config["client_secret"],
                    },
            ) as resp:
                if resp.status != 200:
                    return None

                tokens = await resp.json()

                success = await self.twitter_auth_dao.update_tokens(
                    auth_id=auth.id,
                    access_token=tokens["access_token"],
                    refresh_token=tokens["refresh_token"],
                    expires_at=datetime.utcnow() + timedelta(seconds=tokens["expires_in"]),
                )

                return auth if success else None

    async def _exchange_code(self, code: str, state_data: dict) -> Optional[dict]:
        code_verifier = state_data.get('code_verifier')

        async with aiohttp.ClientSession() as session:
            try:
                print(f"Exchanging code: {code}")
                auth_str = f"{self.oauth_config['client_id']}:{self.oauth_config['client_secret']}"
                async with session.post(
                        "https://api.twitter.com/2/oauth2/token",
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Authorization": "Basic " + base64.b64encode(auth_str.encode()).decode()
                        },
                        data={
                            "code": code,
                            "grant_type": "authorization_code",
                            "client_id": self.oauth_config["client_id"],
                            "client_secret": self.oauth_config["client_secret"],
                            "redirect_uri": self.oauth_config["redirect_uri"],
                            "code_verifier": code_verifier,  # 使用存储的 code_verifier
                        },
                ) as resp:
                    if resp.status != 200:
                        error_message = await resp.text()
                        print(f"Error: Received status code {resp.status}, Details: {error_message}")
                        return None
                    return await resp.json()
            except aiohttp.ClientError as e:
                print(f"Error connecting to Twitter API: {e}")
                return None