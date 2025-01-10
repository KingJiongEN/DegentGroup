from .base_prompt import BasePrompt


class PlanPrompt(BasePrompt):
    
    PROMPT = '''
        You are {name}.
        Your interaction history : {full_interaction_history}
        Your core values are: {core_values} 
        Your understanding of others is : {social_relations}
        Your thoughts_to_do: {unplanned_thoughts}
        
        You need to add expectations for each thoughts_to_do 
        
        You must follow the following criteria: 
        1) each expect should be a simple sentence with a subject-verb-object structure.
        2) the first expect_reeult should be 'I did sth' , strictly comfirm to the thought_to_do
        3) Return the sentence in the JSON format as these examples:
        返回的key 用英文， value用简体中文
        example: 
    
        {EXAMPLE}

    '''
    
    EXAMPLE = {
    "thought_expectations":[
        {"thought_to_do": "@Mr Li, ask why he support the monitor.",
        "expect_reeults": [ "I ask Mr Li about the reason." ,"Mr Li explains the reason", "the reason has explainability",], },
        {"thought_to_do": "@Mr Zhou, ask him to stop spreading the rumor.",
        "expect_results": ["I ask Mr Zhou to stop spreading the rumor", "Mr Zhou says he will stop spreading the rumor."],},
        {"thought_to_do": "@Mr Wang, ask him to quit our group.", 
        "expect_results": ["I ask Mr Wang to quit our group.", "Mr Wang quit our group."]},]
    }
    
    def __init__(self, prompt_type='plan_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        self.set_recordable_key('thought_expectations')
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)