import asyncio
from io import BytesIO
import requests
from typing import Optional, Union
from openai import OpenAI
from teleAgent.core.config import settings

async def generate_image(
    prompt: str,
) -> Union[bytes, None]:
    """
    Generate image using OpenAI's DALL-E model
    
    Args:
        prompt: Image generation prompt
        style: Optional art style to apply
        
    Returns:
        Generated image as bytes or None if generation fails
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    try:
        response = client.images.generate(
            model="dall-e-3", #TODO: for test only
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url",
            quality="standard",
            user="trader_ai"
        )
        
        if not response or not response.data:
            return None
            
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        
        if image_response.status_code != 200:
            return None
            
        return image_response.content
            
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    out = asyncio.run(generate_image("a beautiful image of a cat"))
    breakpoint()
