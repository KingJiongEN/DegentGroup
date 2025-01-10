from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from urllib.parse import unquote
from injector import Injector
from teleAgent.core.di import get_injector
from teleAgent.services.twitter_agent_service import TwitterAgentService
import base64
from teleAgent.services.interfaces import ITwitterAuthService
import json
import re
import logging

router = APIRouter(prefix="/twitter")
templates = Jinja2Templates(directory="teleAgent/templates")

class AuthUrlRequest(BaseModel):
    agent_id: str

@router.get("/auth", response_class=HTMLResponse)
async def twitter_auth_page(request: Request):
    """Render Twitter authorization page"""
    return templates.TemplateResponse(
        "twitter_auth.html",
        {"request": request}
    )

@router.post("/auth-url")
async def get_auth_url(
    req: AuthUrlRequest,
    injector: Injector = Depends(get_injector),
) -> dict:
    """Get Twitter OAuth URL"""
    auth_service = injector.get(ITwitterAuthService)

    try:
        url = await auth_service.create_oauth_url(req.agent_id)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback")
async def twitter_callback(
        code: str,
        state: str,
        injector: Injector = Depends(get_injector),
):
    # Print received state for debugging
    print(f"Received state: {state}")

    try:
        # Define regex pattern to match agent_id, state, and code_verifier
        pattern = r'\{agent_id:\s*([^\s}]+)\s+state:\s*([^\s}]+)\s+code_verifier:\s*([^\s}]+)\}'
        match = re.match(pattern, state)
        if not match:
            raise ValueError("State 格式无效")

        agent_id, state_value, code_verifier = match.groups()

        print(f"Extracted agent_id: {agent_id}, state: {state_value}, code_verifier: {code_verifier}")

        auth_service = injector.get(ITwitterAuthService)
        auth = await auth_service.handle_callback(
            agent_id=agent_id,
            code=code,
            state=state_value,
            code_verifier=code_verifier
        )

        if not auth:
            raise HTTPException(status_code=400, detail="Authentication failed")

        return {"status": "success"}

    except Exception as e:
        print(f"Error parsing state: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid state: {e}")

@router.post("/trigger-test")
async def trigger_test(
    injector: Injector = Depends(get_injector),
) -> dict:
    """Trigger tests for TwitterAgentService"""
    twitter_agent_service = injector.get(TwitterAgentService)

    auth_id = "your_auth_id"
    tweet_text = "Hello, this is a test tweet!"
    tweet_id = "tweet_id_to_reply_to"
    reply_text = "This is a test reply!"

    try:
        # Post a tweet
        post_response = await twitter_agent_service.post_tweet(auth_id, tweet_text)
        if post_response is None:
            raise ValueError("Failed to post tweet")
        logging.info("Post Tweet Response: %s", post_response)

        # Reply to a tweet
        reply_response = await twitter_agent_service.reply_to_tweet(auth_id, reply_text, tweet_id)
        if reply_response is None:
            raise ValueError("Failed to reply to tweet")
        logging.info("Reply Tweet Response: %s", reply_response)

        # Read a tweet
        read_response = await twitter_agent_service.read_tweet(auth_id, tweet_id)
        if read_response is None:
            raise ValueError("Failed to read tweet")
        logging.info("Read Tweet Response: %s", read_response)

        return {
            "post_response": post_response,
            "reply_response": reply_response,
            "read_response": read_response
        }
    except Exception as e:
        logging.error("Error during test trigger: %s", e)
        raise HTTPException(status_code=500, detail=str(e))