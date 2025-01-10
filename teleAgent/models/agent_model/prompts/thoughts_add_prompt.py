from .base_prompt import BasePrompt


class ThoughtsAddPromptV1(BasePrompt):
    
    PROMPT = '''
        You are {name}. 
        Your interaction history : {full_interaction_history}
        Your inner states: {inner_states}
        
        Based on your interaction history, and your understanding of others. Describe the things you want to solve in the next conversation.
        
        You must follow the following criteria:  
        1. Describe the unexpected content. No need to describe existing situation in quick thoughts 
        2. Describe the previous thoughts. 
        3. Describe a unexpected level, ranging from 0 to 10.
        4. Find an object to talk, a specific name or @all
        5. Determine the next step (thought) to do, or just wait for more information. Your next step follow your core values.
        6. analyse if the new next step have already existed in your thoughts_to_do.
        7. Do not add thoughts similar to existing thoughts_to_do. If there is nothing new, keep next steps empty.
        8. decide which channel will the act happen, public or private. Public channel means your words will have influence on all other participants, while private channel means your words can only be read by your direct message object. 
        9. return in the json format,  返回的key 用英文， value用简体中文:
        Here are some examples: 
        1.
         
        {EXAMPLE}

    '''
    
    EXAMPLE = {
        "unexpected_content": "Mr Li is willing to help me.",
        "previous_thoughts": "Mr Li is not satisfied with me.",
        "unexpected_level": 7,
        "next_steps": [{
                        "act_object": "Mr Li",
                        "thought": "observe Mr Li's future behavirous",
                        "does_similar_thoughts_exist": "yes",
                        "channel": "public", 
                        },
                       {
                        "act_object": "@Mr Li",
                        "thought": "show my appreciation to Mr Lin.",
                        "does_similar_thoughts_exist": "no",
                        "channel": "public", 
                       },
                       {
                        "act_object": "Mr Zhou",
                        "thought": "ask what happened to Li that may changed Li's behavior.",
                        "does_similar_thoughts_exist": "no",
                        "channel": "private",
                       },
                       {
                        "act_object": "@all",
                        "thought": "show my support to Mr Lin.",
                        "does_similar_thoughts_exist": "no",
                        "channel": "public",
                       },
        ]
    }
    
    def __init__(self, prompt_type='thoughts_add_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        self.set_recordable_key(['next_steps', 'unexpected_level' ])
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)
    
class ThoughtsAddPrompt(BasePrompt):
    
    PROMPT = '''
        You are {name}.
        Your interaction history : {full_interaction_history}
        Your inner states: {inner_states}
        
        Based on your interaction history, and your understanding of others. Describe the things you want to do in the next conversation.
        
        You must follow the following criteria:  
        1. Describe the interaction history that leads to your next steps, like unepxected content, plans, agreements, etc.
        2. Find an object to talk, a specific name or @all
        3. Determine the next step (thought) to do, or just wait for more information. Your next step follow your core values.
        4. analyse if the new next step have already existed in your thoughts_to_do.
        5. Do not add thoughts similar to existing thoughts_to_do. If there is nothing new, keep next steps empty.
        6. decide which channel will the act happen, public or private. Public channel means your words will have influence on all other participants, while private channel means your words can only be read by your direct message object. 
        7. return in the json format,  返回的key 用英文， value用简体中文:
        Here are some examples: 
        1.
         
        {EXAMPLE}

    '''
    
    EXAMPLE = {
        "next_steps": [{
                        "act_object": "Mr Li",
                        "observation": "Mr Li is willing to help me.",
                        "why_need_further_steps": "It is an unexpected situation since Mr Li is not satisfied with me.",
                        "thought_to_do": "observe Mr Li's future behavirous",
                        "does_similar_thoughts_exist": "yes",
                        "channel": "public", 
                        },
                       {
                        "act_object": "Mr Zhou",
                        "observation": "Mr Li is willing to help me.",
                        "why_need_further_steps": "It is an unexpected situation since Mr Li is not satisfied with me.",
                        "thought_to_do": "ask what happened to Li that may changed Li's behavior.",
                        "does_similar_thoughts_exist": "no",
                        "channel": "private",
                       },
                       {
                        "act_object": "@all",
                        "observation": "I agree to show my support to Mr Lin in the public channel.",
                        "why_need_further_steps": "I have made an agreement with Mr Lin to show my support.",
                        "thought_to_do": "show my support to Mr Lin.",
                        "does_similar_thoughts_exist": "no",
                        "channel": "public",
                       },
        ]
    }
    
    def __init__(self, prompt_type='thoughts_add_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        self.set_recordable_key(['next_steps',])
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)