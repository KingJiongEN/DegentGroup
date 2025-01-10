'''
This module decides if the agent need to response to the group chat or just wait. 
'''

from autogen import ConversableAgent
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent
import autogen
from teleAgent.models.agent_model.prompts.pause_prompt import PausePrompt

class PauseModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=PausePrompt, *args, **kwargs):
        super().__init__(
            name='pause_module',
            system_message="You are a helpful agent in a conversation. Check if you need to response to the group chat or just wait.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.response_decision)
        
  
    def response_decision(self, message_dict, recipient):
        recipient.working_memory['response_decision'] = message_dict['response_decision']
        self.logger.info(f"{recipient.name} response_decision: {message_dict}")
        return dict()