'''
this prompt remove solved thoughts and TODO update world model
'''
from .base_prompt import BasePrompt


class ThoughtsSolvePrompt(BasePrompt):
    
    PROMPT = '''
        You are {name}. 
        Your interaction history : {full_interaction_history}
        Your previous thoughts_to_do: {thoughts_to_do}
        Your personality: {personality}
        Your poet_art_preference: {poet_art_preference}
                
        Based on your interaction history, your understanding of others. Remove the finished thoughts in thoughts_to_do list. 
        
        You should analyse each thoughts in previous thoughts_to_do by the follwoing steps:
        1. Question current situation. Ask if the current situation meets the expect results, answer based on the interation history.
        2. Summary the compeletion of previous thoughts, and think about the next steps based on your core values
        3. The next step should be only with a single imperative action, no 'and', 'or'
        4. If the previous thought is 100 percent completed, or it has not been started yet, keep the next_steps list empty.
        5. for thoughts that have been totally solved or partially solved but with clear next steps, put them into thought_to_remove_list.
        6. Do not put thoughts that are not solved at all into thought_to_remove_list
        7. gather next_steps of all previous thougts 
        8. return in the json format,  返回的key 用英文， value用简体中文:
        return example:
        {EXAMPLE}

    '''
    
    EXAMPLE = {
        "analysis_each_thoughts": [{"prev_thought_to_do": "@Mr Li, ask why he support the monitor.",
                                    "expect_results": [ "I ask Mr Li about the reason." ,"Mr Li explains the reason", "the reason has explainability",], 
                                    "question_current_situation":[
                                            {
                                                "question": "Did I ask Mr Li about the reason?",
                                                "answer": "Yes. I ask Mr Li about the reason.",
                                            },
                                            {
                                                "question": "Does Mr Li explain the reason ?",
                                                "answer": "Yes, Mr Li explains that he believes in the monitor's personality.",
                                            },
                                            {
                                                "question": "Does the reason has explainability?",
                                                "answer": "No. From my understanding, Mr Li does not believe in the monitor.",
                                            }
                                    ],
                                    "summary_and_think_about_next_steps": "The credibility of  Mr Li's reason is questionable. Considering my core value: people should earn reputaion by their abilities." ,
                                   "next_steps": [{"thought": "@Mr Li, ask why he believes in the monitor's personality.", "act_channel": "public"}],
                                   },
                                  {"prev_thought_to_do": "@Mr Zhou, ask him to stop spreading the rumor.",
                                   "expect_results": ["I ask Mr Zhou to stop spreading the rumor", "Mr Zhou says he will stop spreading the rumor."],
                                    "question_current_situation": [
                                        {
                                          "question": "Do I ask Mr Zhou to stop spreading the rumor? ",
                                          "answer": "Yes. I said @Mr Zhou, spreading rumor is not good for your reputation."
                                        },
                                        {"question": "Does Mr Zhou say he will stop spreading the rumor?",
                                        "answer": "Yes. Mr Zhou said he will never do it again. ",
                                        },                                        
                                    ],
                                    "summary_and_think_about_next_steps": "I have finished it." ,
                                    "next_steps": []
                                  },
                                  {
                                    "prev_thought_to_do": "@Mr Wang, ask him to quit our group.", 
                                    "expect_results": ["I ask Mr Wang to quit our group.", "Mr Wang quit our group."],
                                    "question_current_situation": [
                                        {
                                            "question": "Do I ask Mr Wang to quit our group?",
                                            "answer": "Yes, I said it is better that Mr Wang quit our group since he is not qualitfied.",
                                        },
                                        {
                                            "question": "Does Mr Wang quit our group?", 
                                            "answer": "No. Mr Wang insist on staying in the group."
                                        }
                                    ],
                                    "summary_and_think_about_next_steps": "I asked with politeness but Mr Wang does not respect my willingness. Considering my core value: people should earn reputaion by their abilities." ,
                                    "next_steps": [{"thought": " @ Mr Wang, ask him to quit our group with sarcastic words,", "act_channel": "public"}]
                                  }
                                ],
        "thought_to_remove_list": ["@Mr Li, ask why he changed his mind.", "@Mr Zhou, ask him to stop spreading the rumor.", "@Mr Wang, ask him to quit our group."],
        "next_steps": [{"thought": "@Mr Li, ask why he believes in the monitor's personality.", "act_channel": "public"}, {"thought": " @ Mr Wang, ask him to quit our group with sarcastic words,", "act_channel": "public"}]
    }
    
    def __init__(self, prompt_type='thoughts_solve_prompt') -> None:
        super().__init__( prompt_type=prompt_type, check_exempt_layers=[3,4,5,6,7] )
        self.set_recordable_key(['thought_to_remove_list', 'next_steps'])
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)