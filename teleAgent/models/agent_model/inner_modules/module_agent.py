import inspect
import json
import os
from typing import Any, Dict, List, Optional
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.text_compressors import LLMLingua
from autogen.agentchat.contrib.capabilities.transforms import TextMessageCompressor
from autogen import ChatResult
from datetime import datetime
import logging
import copy

from teleAgent.models.agent_model.utilities.function_chain import FunctionChain
from teleAgent.models.agent_model.prompts.base_prompt import BasePrompt
from teleAgent.constants import DATA_STORE_ROOT
from teleAgent.logger.logger import shared_logger, setup_logger

class CognitiveModuleAgent(AssistantAgent):
    '''
    The cognitive module is an LLM agent with a specific cognitive funciton. 
    Its function and return format is defined in functional_prompt. And it only response once, no conversation.
    It has a function chain to process the response.
    '''
    def __init__(self, functional_prompt:BasePrompt, *args, **kwargs):
        super().__init__(
            # max_consecutive_auto_reply=2,
            *args, **kwargs)
        # self.register_lingua()
        self.logger = shared_logger #setup_logger(name=self.name, log_files=[ f'{DATA_STORE_ROOT}/logs/main.log'], level=logging.DEBUG, console=True)
        self.functional_prompt:BasePrompt = functional_prompt()
        self.function_chain = FunctionChain()
        self.function_chain.add(self.load_message)
        # self.function_chain.add(self.data_store)
        self.register_hook('process_message_before_send', CognitiveModuleAgent.post_chats_functions)
        
    def register_lingua(self):
        llm_lingua = LLMLingua()
        text_compressor = TextMessageCompressor(text_compressor=llm_lingua)
        context_handling = transform_messages.TransformMessages(transforms=[text_compressor])
        context_handling.add_to_agent(self)
    
    async def a_generate_reply( self, 
                                messages: Optional[List[Dict[str, Any]]] = None,
                                sender: Optional["Agent"] = None,
                                restart_times=0,
                                **kwargs: Any,):
        reply = await super().a_generate_reply(
                            messages=messages,
                            sender=sender,
                            **kwargs,    
                            )
        error = self.functional_prompt.response_format_check(reply, check_exempt_layers=self.functional_prompt.check_exempt_layers)
        if error:
            self.logger.error(f'Error in response: {error}.')
            
            if messages is None:   
                messages = self._oai_messages[sender]
            messages[-1]['content'] =  messages[-1]['content'] + f'\n # '+  error +' Please strictly follow the example in the prompt'
            
            restart_times += 1 
            if restart_times < 4:
                return await self.a_generate_reply(messages=messages, sender=sender, restart_times=restart_times, )  
        
        return reply
    
    @staticmethod
    def post_chats_functions(sender, message, recipient, silent):
        # sender is self
        success, return_dict = sender.function_chain.execute(obj=sender,**{
            'message': message,
            'sender': sender,
            'recipient': recipient,
            'silent': silent
        }) 
        if success:
            message = return_dict.get('message', message)
        return message
   
    def load_message(self, message:str):
        message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        return {'message_dict': message_dict}

    def data_store(self, message:str):
        store_path = f'{DATA_STORE_ROOT}/modules'
        os.makedirs(store_path,exist_ok=True) 
        time_str = datetime.now().strftime("%m-%d-%H-%M-%S")
        for sender in self.chat_messages:
            instruction_data =  copy.deepcopy(self.chat_messages[sender])
            instruction_data.append({'role':'assistant', 'content': message})
        
            with open(f'{store_path}/{sender.name}_{self.name}_{time_str}.json', 'w') as f:
                json.dump(instruction_data, f, ensure_ascii=False, indent=4)
            return dict()
        