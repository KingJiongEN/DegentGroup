from autogen import ConversableAgent
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent
from teleAgent.models.agent_model.prompts.summary_prompt import SummaryPrompt

class SummaryModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=SummaryPrompt, *args, **kwargs):
        super().__init__(
            name='summary_module',
            system_message="You are a helpful agent in a conversation. Check if you need to response to the group chat or just wait.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.add_summary)
        
  
    def add_summary(self, message_dict, recipient):
        assert message_dict['chat_type'] in ['groupchat', 'privatechat']
        if message_dict['chat_type'] == 'groupchat':
            recipient.working_memory.update({'groupchat_summary': message_dict['summary']})
        else:
            participant = message_dict['participants'][0] 
            if 'privatechat_summary' not in recipient.working_memory:
                recipient.working_memory['privatechat_summary'] = dict()
            recipient.working_memory['privatechat_summary'].update({ participant: message_dict['summary']})
        self.logger.info(f"{recipient.name} groupchat_summary: {message_dict}")
        return dict()