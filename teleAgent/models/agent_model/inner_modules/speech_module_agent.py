import asyncio
import os
import time
import uuid
import autogen
import httpx
import openai
import replicate
from autogen import ConversableAgent, AssistantAgent, Agent
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union
from pathlib import Path

from teleAgent.models.agent_model.utilities.small_tools import get_audio_duration, keep_latest_k_files
from teleAgent.logger.logger import shared_logger

openai_api = os.getenv('OPENAI_API_KEY', 'sk-proj-1314134') # place holder

class SpeechModuleAgent:
    def __init__(self, 
            speech_api_config: Optional[Union[Dict, Literal[False]]],
        ):
        """
        speech_api_config contains the name of api , and other parts should be a dict that strictly mathes the api call's kwargs
        """
        
        self.model_name = speech_api_config.get('model_name')
        if self.model_name == 'openai':
            self.client = openai.OpenAI(api_key=speech_api_config.get('api_key', openai_api))
        self.model_call = {
            'openai': self.a_openai_call,
            'chat_tts': self.chat_tts_call,
        }[self.model_name]
        
        self.speech_api_config:dict = speech_api_config['tts_model_config']
   
    async def __call__(self, message:str, *args: Any, **kwds: Any) -> Any:
        time1 = time.time()
        outinfo = await self.model_call(message, *args, **kwds,)
        time2 = time.time()
        time_cost = time2 - time1
        return dict(time_cost=time_cost, outinfo=outinfo)
            
    async def chat_tts_call(self, 
                message,
                ) -> Dict[str, Any]:
        '''
        input kwargs
            {
                "text": message,
                "top_k": 20,
                "top_p": 0.7,
                "voice": 2222,
                "prompt": "",
                "skip_refine": 0,
                "temperature": 0.3,
                "custom_voice": 0
            }
        
        '''
        
        model_kwargs = {'text': message}
        model_kwargs.update(self.speech_api_config)
        output = replicate.run(
            "thlz998/chat-tts:fdb4f547d19c9591d7e0223c88b14886c110129c0e206ddbb97fe7a344162868",
            input=model_kwargs,
        )
        output.update(
            {
                'model': 'chat_tts',
                'message': message,
                'filename': message['filename']
            }
        )
        return output
        
    async def a_openai_call(self, message):
        try:
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {openai_api}",
                "Content-Type": "application/json"
            }
            
            model_kwargs = {'input': message}
            model_kwargs.update(self.speech_api_config)
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=model_kwargs)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Check the content type to handle the response appropriately
                content_type = response.headers.get("Content-Type")
                
                if "application/json" in content_type:
                    return response.json()  # Return JSON if the response is JSON
                elif "audio/mpeg" in content_type or "audio/mp3" in content_type:
                    # Save the binary content as an MP3 file
                    uuidv = uuid.uuid1()
                    static_folder = Path("static")
                    output_path = static_folder / f"audio_record"
                    with open( output_path/f"{uuidv}.mp3", "wb") as f:
                        f.write(response.content)
                    mp3_duration = get_audio_duration(output_path/f"{uuidv}.mp3")
                    mp3_duration = 0
                    keep_latest_k_files(output_path, 5)
                    return {
                        "filename": str(output_path/f"{uuidv}.mp3"), 
                        "content": message,
                        "model": "openai",
                        "audio_duration": mp3_duration,
                    }
                else:
                    raise ValueError(f"Unsupported content type: {content_type}")
        except Exception as e:
            shared_logger.error(f"Error in openai tts call: {e}")
            
if __name__ == '__main__':
    speech_api_config = {
        'model_name': 'openai',
        'tts_model_config':{
            "model": "tts-1",
            "voice": "nova",
        }
    }
    module = SpeechModuleAgent(speech_api_config)
    asyncio.run(module('吃葡萄不吐葡萄皮。'))