from autogen import ConversableAgent
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent
import autogen
from teleAgent.models.agent_model.prompts.emotion_prompt import EmotionPrompt
from teleAgent.models.agent_model.inner_modules.emotion import Emotion
from teleAgent.logger.logger import shared_logger

class EmotionModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=EmotionPrompt, *args, **kwargs):
        super().__init__(
            name='emotion_module',
            system_message="You are an emotion module, you can update and check the emotion of the agents.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.extract_contents)
        self.function_chain.add(self.update_emotion)
        
    def extract_contents(self, message_dict):
        # message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        self.logger.info(message_dict)
        return  dict(( k, message_dict[k]) for k in self.functional_prompt.recordable_key)
    
    @staticmethod
    def update_emotion(emotions, recipient):
        shared_logger.info(f" updating {recipient.name} emotion")
        recipient.emotion.update(emotions)
        return dict()

if __name__ == '__main__': 
    pass