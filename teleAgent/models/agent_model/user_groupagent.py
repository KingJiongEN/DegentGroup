import asyncio
import json
from autogen import ConversableAgent, Agent, AssistantAgent, UserProxyAgent, ChatResult
from autogen.cache import AbstractCache
from autogen.agentchat.utils import consolidate_chat_info, gather_usage_summary

from teleAgent.models.agent_model.simutan_group import SimutanGroup
from teleAgent.models.agent_model.proact_groupagent import ProactGroupAgent
from typing import Callable, List, Dict, Optional, Union

class UserGroupAgent(ProactGroupAgent):
    '''
    the proact group agent will proactively get the message from the group chat
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(
            human_input_mode = 'ALWAYS',
            llm_config=False,
            code_execution_config={"use_docker": False},
            *args, **kwargs)
        
    async def a_init_group_chat(self):
        pass

    async def a_send(self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        '''
        raw a_send, unchanged
        '''
        message = self._process_message_before_send(message, recipient, silent)
        # When the agent composes and sends the message, the role of the message is "assistant"
        # unless it's "function".
        valid = self._append_oai_message(message, 'assistant', recipient)
        if valid:
            await recipient.a_receive(message, self, request_reply, silent)
        else:
            raise ValueError(
                "Message can't be converted into a valid ChatCompletion message. Either content or function_call must be provided."
            )