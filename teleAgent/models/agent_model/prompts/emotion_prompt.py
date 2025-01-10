from .base_prompt import BasePrompt


# @register(name=PromptType.EMOTION, type='prompt')
class EmotionPrompt(BasePrompt):
    # TODO: add more categories of emotions such as jealous, pride.
    '''
    More complex emotions can be represented using combinations of the above emotions, for example:
        - agreesiveness = anticipation + anger
        - contempt = disgust + anger
        - remorse = sadness + disgust
        - disapproval = surprise + sadness
        - awe = fear + surprise
        - submission = trust + fear
        - love = joy + trust
        - optimism = anticipation + joy
    '''
    
    #TODO: bullies' emotion : aggressiveness decreases, regret/guilt increases,  finally empathy increases
    
    PROMPT = '''
        Describe the emotion you are currently experiencing.
        Your emotion is built based on the theory of robert plutchik's wheel of emotions, which includes these basic emotions: {emotion_options}.
        
        Select 3 kinds of emotions from the above eight basic emotions to best describe your current emotion.
        For each emotion, describe the change of the emotion intension on a scale of -2 to 2. 

        
        Your previous emotion: {emotion}
        Your personality: {personality}
        Your interaction history : {full_interaction_history}
        
        You must follow the following criteria: 
        1) For previous emotions, 0 means no emotion, 10 means the most intense emotion, 6 means a neutral state. e.g. anger:10 means very angry, sadness:3 means a little bit sad.
        2) You should associate the emotion with the current situation. Consider all the basic emotions in the wheel of emotions, and return at least 3 emotions to modify.
        3) describe the change in intensity of the emotion as the first impression as you witness the situation, and explain the emotion change.
        4) The emotion change should be between -3 and 3. e.g. anger: -5 means the anger is gone, anger: 5 means the anger is very intense.
        5) Return the sentence in the JSON format as this example:
        {EXAMPLE}
    '''
    
    EXAMPLE = {
        "emotions_to_modify": ['joy', 'trust', 'surprise'],
        "emotions": [
            {
                "emotion": "joy",
                "change": 2,
                "explanation": "I feel much happy beacause I get a gift from my friend Jay."
            },
            {
                "emotion": "trust",
                "change": 1,
                "explanation": "Jay consider my status. I trust him."
            },
            {
                "emotion": "anger",
                "change": -2,
                "explanation": " I am not angry anymore because Jay gives me a gift."
            }
        ]
    }
    
    def __init__(self, prompt_type='emotion_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        self.set_recordable_key('emotions')
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)