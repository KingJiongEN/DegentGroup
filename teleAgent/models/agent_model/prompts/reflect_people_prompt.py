from .base_prompt import BasePrompt


class ReflectPeoplePrompt(BasePrompt):
    
    PROMPT = '''
        You are {name}. 
        Your previous understanding of others : {social_relations}
        Your personality: {personality}
        Your poet_art_preference: {poet_art_preference}
        
        #### Your interaction history : {full_interaction_history}
        
        Based on your interaction history, update your understanding of others. Note that seldom people will change their mind. So 
        
        You must follow the following criteria if you observe something unexpected:
        1. determine a specific object from recent interacted objects that you reflect your previous understanding and have new understanding of.  
        2. describe the previous understanding of the object.
        3. describe the unexpected observation that different from your previous understanding.
        4. try to use your previous understanding to explain the unexpected observation.
        5. describe the explanatory power of your previous understanding, from 0-10
        6. describe an alternative explanation as your new understanding of the object based on your core values. If you just want to add some new information, maintain the unchanged part of the previous understanding.
        7. describe the explanatory power of your new understanding, from 0-10 
        8. Analyse totoally based on interaction history. Only the people appear in the chat history. Do not add anything that does not exist in the interaction history.
        return in json format 
        返回的key 用英文， value用简体中文
        
        Here are some examples: 
        1. when you do not find anything beyond your previous understanding, you do not need to update your understanding.
        2. when you find something unexpected, you need to update your understanding. 
        {EXAMPLE}

    '''
    
    EXAMPLE = {
        "recent_object":  ["Mr Li", "Mr Wang", "Mr Zhang"],
        "reflections":
        [
            {
                "reflect_object": "Mr Li",
                "previous_understanding": "Mr Li is knowledgeable and willing to solve all problems.",
                "unexpected_observation": "Mr Li refuses to solve this problem.",
                "unexpectation_level": 8,
                "explain_by_previous_understanding": "It is the first time we see such kind of problems, So Mr Li is not familiar with this problem.",
                "explanatory_power_prev": 7,
                "new_understanding": "Mr Li is knowledgeable and willing to solve most problems, except for the new problems.",
                "explanatory_power_new": 5,
            },
            {
               "reflect_object": "Mr Wang",
                "previous_understanding": "Mr Wang is eager to learn new knowledges.",
                "unexpected_observation": "Mr Wang is asking Mr Zhang questions with politeness.",
                "unexpectation_level": 2,
                "explain_by_previous_understanding": "Mr Wang wants to learn knowledge from Mr Zhang so he shows politeness. ",
                "explanatory_power_prev": 8,
                "new_understanding": "Mr Wang wants to enhance Mr Zhang's impression on him, so he shows politeness.",
                "explanatory_power_new": 4,
            }, 
            {
               "reflect_object": "Mr Zhang",
                "previous_understanding": "Mr Zhang is a kind person, who is well socialized.",
                "unexpected_observation": "Mr Zhang does not respond to Mr Wang's multiple request.",
                "unexpectation_level": 9,
                "explain_by_previous_understanding": "Mr Zhang is too tired to respond.",
                "explanatory_power_prev": 3,
                "new_understanding": "Mr Zhang is a kind person, who is well socialized. But he does not like to be interrupted by unfamiliar people.",
                "explanatory_power_new": 8,
            },  
        ]
    }
    
    def __init__(self, prompt_type='reflect_people_prompt') -> None:
        super().__init__( prompt_type=prompt_type,)
        self.set_recordable_key(['reflections'])
        # self.set_recordable_key(['reflect_object', 'new_understanding','explanatory_power_new', 'explanatory_power_prev' ])
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)