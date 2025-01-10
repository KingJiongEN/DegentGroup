"""
This prompt helps agent perspect the world.
"""

from .base_prompt import BasePrompt

class PerspectPrompt(BasePrompt):
    PROMPT = """
        You are {name}. {chat_condition} 
        Your interaction history : {full_interaction_history}
        
        如果你在群聊中
        Add the new information into the old summary. Do not change the previous summary too much.
        return in json format:
        返回的key 用英文， value用简体中文
        
        {EXAMPLE}
        
        如果你在私聊中， 回复json 
        {
            "updated_summary": "null"
        }
    """
    
    EXAMPLE = {
        "involved_participants": [],
        "updated_summary": " Mr Wang re I asked Mr Zhang for help.  "
    }