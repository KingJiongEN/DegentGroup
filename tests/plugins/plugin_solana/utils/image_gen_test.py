# tests/plugins/plugin_solana/utils/test_image_gen.py

import os
import pytest
import time

from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.utils.image_gen import generate_image

def retry_on_rate_limit(func):
    """Decorator to retry on rate limit errors"""
    async def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise
    return wrapper


@skip_in_github_actions
@pytest.mark.integration
@pytest.mark.asyncio
@retry_on_rate_limit
async def test_generate_image_pop_art():
    """Test image generation with pop art style"""
    prompt = "A cat sitting on a chair"
    result = await generate_image(prompt, "pop_art")
    
    assert result is not None
    assert len(result) > 0