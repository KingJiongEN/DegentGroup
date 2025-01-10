from .base_prompt import BasePrompt


class ReflectInteractionPrompt(BasePrompt):
    
    PROMPT = '''
        You are {name}. 
        Your interaction history : {full_interaction_history}
        Your previous understanding of others: {social_relations}
        Your core values: {core_values}
        
        Update your interaction pattern with the object , based on your interaction history, previous understanding of the object, new understanding of the object 
        
                
        You must follow the following criteria if you observe something unexpected:
        1. compare your previous understanding with the new understanding of the object.
        2. generate how to update your interaction pattern based on the comparison and your core values.
        3. Update the interaction pattern following the comparison you made before.
        4. Note that in most cases you should maintain some parts in the old interaction pattern.
        5. Analyse totoally based on interaction history. Only the people appear in the chat history. Do not add anything that does not exist in the interaction history.
        6. return in json format
         返回的key 用英文， value用简体中文
        
        Here are some examples: 
        1. when there is no new understanding, you do not need to update your interaction pattern.
        2. otherwise, update the interaction pattern in the json format as below:
        
        
    
        {EXAMPLE}

    '''
    
    EXAMPLE = {
        'reflections':[
           { 
                "reflect_object": "Mr Li",
                "previous_understanding": "Mr Li is knowledgeable and willing to solve all problems.",
                "new_understanding": "Mr Li is knowledgeable and willing to solve most problems, except for the new problems.",
                "old_interaction_pattern": "Once I have a problem, ask Mr Li for help since he will solve it.",
                "how_to_update_interaction_pattern": "Since Mr Li is unwilling to solve new problems, I will ask him for help only when I have old problems.",
                "new_interaction_pattern": "Once I have a problem, check if it is a new problem, if not, ask Mr Li for help since he will solve it.",
            },
           {
                "reflect_object": "Mr Zhang",
                "previous_understanding": "Mr Zhang is a kind person, who is well socialized.", 
                "new_understanding": "Mr Wang is a kind person, who is well socialized. But he does not like those students from poor families like Mr Wang.",
                "old_interaction_pattern": "Share everything with Mr Zhang.",
                "how_to_update_interaction_pattern": "Since he does not like those students from poor families, I will not introduce people from poor background to him. ",
                "new_interaction_pattern": "Share everything with Mr Zhang. Avoid introducing students from poor families to him."
           }
        ],
    }
    
    def __init__(self, prompt_type='reflect_interaction_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        self.set_recordable_key(['reflections' ])
        # self.set_recordable_key(['reflect_object', 'new_understanding', 'new_interaction_pattern' ])
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)