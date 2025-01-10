import asyncio
import copy
from datetime import datetime
import httpx
from openai import OpenAI
import replicate
from dataclasses import dataclass, field
import json
import os
import shutil
import pandas as pd
from typing import Optional, List, Dict, Union, Type
from autogen import GroupChat, GroupChatManager, Agent, AssistantAgent, ConversableAgent
from autogen.code_utils import content_str
from autogen.agentchat.groupchat import NoEligibleSpeaker
from datetime import datetime, timedelta

from teleAgent.models.agent_model.utilities.serialization import CustomJSONEncoder
from teleAgent.constants import DATA_STORE_ROOT
from teleAgent.models.agent_model.utilities.small_tools import extract_json_from_markdown, rollback_to_time
from teleAgent.models.agent_model.prompts.analyse_prompt import AnalysePrompt
from teleAgent.models.agent_model.inner_modules.analyse_module_agent import AnalyseModuleAgent
from teleAgent.logger.logger import shared_logger

@dataclass
class SimutanGroup(GroupChat):

    human_agent:AssistantAgent = field(default=None)
    speakout:bool = field(default=False)
    messages_and_states:List[Dict] = field(default_factory=list)
    backup_datasets:Dict = field(default_factory=dict)
    analyse_module:Optional[Agent] = field(default=AnalyseModuleAgent())
    resource:Optional[str] = field(default=None)
    def __post_init__(self, messages_csv='groupchat.csv'):
        super().__post_init__()
        self.data_store_root = DATA_STORE_ROOT
        self.messages_csv = DATA_STORE_ROOT / messages_csv
        # if os.path.exists(self.data_store_dir):
        #     shutil.rmtree(self.data_store_dir)
        os.makedirs(self.data_store_root, exist_ok=True)
        
        if self.human_agent is not None and self.human_agent not in self.agents:
            self.agents.append(self.human_agent)
            
        for agent in self.agents:
            agent.register_groupchat(self)
            if agent.human_input_mode == 'ALWAYS':
                assert agent == self.human_agent, f'Only one agent can be human agent. {agent.name} is not human agent.'

        # self.complete_timestamps()
        self.update_all_agent_states()

    @property
    def update_count(self):
        return len(self.messages)
            
    def update_agent_states(self, agent_name): # better to be a sql
        agent = self.agent_by_name(agent_name)
        if hasattr(agent, 'inner_states'):
            new_inner_stats = agent.inner_states
            if new_inner_stats is None: shared_logger.error(f'No inner states found for {agent_name}')
            for inner_prop in new_inner_stats: 
                inner_prop_store_path = f'{self.data_store_root}/{inner_prop}.json'
                existing_states = {}
                if os.path.exists(inner_prop_store_path):
                    with open(inner_prop_store_path, 'r') as f:
                        existing_states = json.load(f)
                existing_states[agent_name] = json.dumps(new_inner_stats[inner_prop], cls=CustomJSONEncoder, ensure_ascii=False)
                        
                with open(inner_prop_store_path, 'w') as f:
                    json.dump(existing_states, f, indent=2,  cls=CustomJSONEncoder, ensure_ascii=False)
    
    def update_all_agent_states(self):
        for agent_name in self.agent_names:
            self.update_agent_states(agent_name)
    
    def present_new_message(self, message:Dict):
        if os.getenv('DEBUG'):
            shared_logger.info(f"{message}")
        df = pd.DataFrame.from_records(self.messages_and_states)
        df.to_csv(self.messages_csv, index=False)
    
    async def update_messages(self, reply:Dict, speaker:Agent):
        if 'timestamp' not in reply: reply['timestamp'] = speaker.timestamp
        self.append(reply,speaker=speaker)
        if len(self.messages_and_states) > 40:
            self.messages_and_states = self.messages_and_states[:3] + self.messages_and_states[-37:]
            self.messages = self.messages[:3] + self.messages[-37:]
        # self.present_new_message(reply,)
        
        return self.update_count
     
    def append(self, message: Dict, speaker: Agent):
        # if message["role"] != "function":
        #     message["name"] = speaker.name
        # message["content"] = content_str(message["content"])
        # self.messages.append(message)
        
        super().append(copy.deepcopy(message), speaker)
        # append to messages_and_states
        
        message.update(speaker.inner_states_dict)
        self.messages_and_states.append(message)
     
    async def a_get_human_input(self, user_input:str):
        # interface to receive human input from client
        await self.update_messages({'role':self.human_agent.name, 'content':user_input}, speaker=self.human_agent)
        return 'success'
    
    async def a_direct_message(
        self, 
        recipient: Union[ConversableAgent, str], 
        message: str, 
        sender: Union[ConversableAgent, str, None] = None
    ):
        if sender is None:
            assert self.human_agent is not None, 'human agent is not found and sender is not provided'
            sender = self.human_agent 
        else:
            if type(sender) is str:
                sender = self.agent_by_name(sender)
        
        if type(recipient) is str:
            recipient = self.agent_by_name(recipient)
        
        assert recipient.human_input_mode == 'NEVER', f'recipient should not be human agent, now is {recipient.name}'
        reply = await sender.a_initiate_chat(message=message, recipient=recipient, max_turns=1, 
                                            summary_method='last_msg',
                                            silent=False if os.getenv('DEBUG') else True,
                                            clear_history=False,
                                            )

        message4cilent = {'content':reply.summary, 'role': recipient.name, 'channel': "dm-chat", 'avatar': recipient.avatar}
            
        await message_queue.put(json.dumps(message4cilent,ensure_ascii=False))
        queue_size = message_queue.qsize()
        await asyncio.sleep(0.5*queue_size)
        shared_logger.info(f'queue size {message_queue.qsize()}')

        # return reply
    
    def get_dm_history(self, recipient:"ProactGroupAgent", sender:ConversableAgent=None):
        if sender is None:
            assert self.human_agent is not None, 'human agent is not found and sender is not provided'
            sender = self.human_agent 
        else:
            sender = self.agent_by_name(sender)
        recipient = self.agent_by_name(recipient)
        
        msg_history = copy.deepcopy(sender.chat_messages[recipient]) # remove system message ?
        for msg in msg_history:
            if msg['content'] == 'TERMINATE': continue
            if msg['role'] == 'assistant':
                msg['role'] = 'You'
            else:
                msg['role'] = recipient.name
            
            content = msg['content']
            try:
                content_dict = eval(content)
                msg['content']  = content_dict['content']
            except:
                pass
        
        return msg_history

    async def a_analyse_human_performance_all(self):
        assert self.human_agent is not None, 'human agent is not found'
        self.suspend_chat()
        # handle group chat
        if len(self.messages_and_states) == 0: return
        group_chat_msg_hist = [] 
        messages_and_states = copy.deepcopy(self.messages_and_states)
        for msg in messages_and_states:
            if msg['role'] == self.human_agent.name:
                msg['role'] = 'User'
            group_chat_msg_hist.append(msg)
            # group_chat_msg_hist.append({'role': msg['role'] , 'content': msg['content'], 'timestamp': msg['timestamp']}) 
            
        group_chat_analyse_task = asyncio.create_task(self.a_analyse_human_performance_single(group_chat_msg_hist, self.human_agent, save_json_filename='group_chat.json'))
        
        # handle chat for each agent
        for recipeint in list(self.human_agent.chat_messages.keys()):
            if recipeint == self.analyse_module: continue
            msg_history_raw = recipeint.chat_messages[self.human_agent]
            msg_history = copy.deepcopy(msg_history_raw)  
            msg_ls = []
            for msg in msg_history:
                if msg['role'] == 'assistant':
                    msg['role'] = recipeint.name
                msg_ls.append(msg)
                # msg_ls.append({'role': msg['role'] , 'content': msg['content']})
            with open(f'{self.data_store_root}/chat_with_{recipeint.name}.json', 'w') as f:
                json.dump(msg_ls, f, indent=2, ensure_ascii=False)
            await self.a_analyse_human_performance_single(msg_ls, self.human_agent, save_json_filename=f'{recipeint.name}.json')
        
        # handle impression
        impression_from = {}
        for agent in self.agents:
            if agent != self.human_agent:
                impression_from[agent.name] = agent.social_relations.impression_on_name(self.human_agent.name) 

        with open(f'{self.data_store_root}/impression_from_others.json', 'w') as f:
            json.dump(impression_from, f, indent=2, ensure_ascii=False)
        
        if not group_chat_analyse_task.done():
            await group_chat_analyse_task
    
    
    def recall_agent_state(self, agent_name, time_str):
        target_time = datetime.strptime(time_str, TIMESTAMP_FORMAT)
        for msg_id in range(len(self.messages_and_states)-1, -1, -1):
            msg = self.messages_and_states[msg_id]
            recall_time = datetime.strptime(msg['timestamp'], TIMESTAMP_FORMAT )
            speaker = msg.get('role', msg.get('name'))
            if speaker == agent_name and recall_time <= target_time:
                return msg
        shared_logger.info(f'No state found for {agent_name} before {time_str}')
        return dict()
    
    def rollback(self, time):
        self.backup_messages()
        self.messages_and_states = rollback_to_time(self.messages_and_states, time)
        self.messages = rollback_to_time(self.messages, time)
        
        for agent in self.agents: # rollback inner states
            # if agent == self.human_agent: continue
            status = self.recall_agent_state(agent.name, time)
            agent.rollback(time, status)

    def backup_messages(self):
        key = len(self.backup_datasets)
        self.backup_datasets[key] ={ 
                                    "messages": copy.deepcopy(self.messages),
                                    "messages_and_states": copy.deepcopy(self.messages_and_states),
                                    }
        
    
                
class MyGroupManager(GroupChatManager):
    '''
    all agent in the group chat will response to all message
    '''
    
    def __init__(self,
        groupchat: GroupChat,
        name: Optional[str] = "chat_manager",
        max_consecutive_auto_reply: Optional[int] = 20,
        human_input_mode: Optional[str] = "NEVER",
        system_message: Optional[Union[str, List]] = "Group chat manager.",
        silent: bool = False,
        **kwargs,
    ):
        super().__init__(
            groupchat=groupchat,
            name=name,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            system_message=system_message,
            silent=silent,
            **kwargs,
        )
        self.register_reply(Agent,
            MyGroupManager.a_run_chat_refine,
            config=groupchat,
            reset_config=GroupChat.reset,
            ignore_async_in_sync_chat=True,
        )
    
 
    async def a_run_chat_refine(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[GroupChat] = None,
    ):
        """Run a group chat asynchronously."""
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        speaker = sender
        groupchat = config
        send_introductions = getattr(groupchat, "send_introductions", False)
        silent = getattr(self, "_silent", False)
        if send_introductions:
            # Broadcast the intro
            intro = groupchat.introductions_msg()
            for agent in groupchat.agents:
                await self.a_send(intro, agent, request_reply=False, silent=True)
            # NOTE: We do not also append to groupchat.messages,
            # since groupchat handles its own introductions

        if self.client_cache is not None:
            for a in groupchat.agents:
                a.previous_cache = a.client_cache
                a.client_cache = self.client_cache
        for i in range(groupchat.max_round):
            groupchat.append(message, speaker)

            if self._is_termination_msg(message):
                # The conversation is over
                break

            # broadcast the message to all agents except the speaker
            for agent in groupchat.agents:
                if agent != speaker:
                    await self.a_send(message, agent, request_reply=False, silent=True)
            if i == groupchat.max_round - 1:
                # the last round
                break
            try:
                # select the next speaker
                speaker = await groupchat.a_select_speaker(speaker, self)
                # let the speaker speak
                reply = await speaker.a_generate_reply(sender=self)
            except KeyboardInterrupt:
                # let the admin agent speak if interrupted
                if groupchat.admin_name in groupchat.agent_names:
                    # admin agent is one of the participants
                    speaker = groupchat.agent_by_name(groupchat.admin_name)
                    reply = await speaker.a_generate_reply(sender=self)
                else:
                    # admin agent is not found in the participants
                    raise
            except NoEligibleSpeaker:
                break
            # breakpoint()

            if reply is None:
                break
            # The speaker sends the message without requesting a reply
            await speaker.a_send(reply, self, request_reply=False, silent=silent)
            message = self.last_message(speaker)
        if self.client_cache is not None:
            for a in groupchat.agents:
                a.client_cache = a.previous_cache
                a.previous_cache = None
        return True, None
