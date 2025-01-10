# Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
#
# SPDX-License-Identifier: Apache-2.0
import copy
import inspect
import json
import re
import warnings
from dataclasses import dataclass
from enum import Enum
from inspect import signature
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel

from autogen.function_utils import get_function_schema
from autogen.oai import OpenAIWrapper

from autogen import Agent, ChatResult, ConversableAgent, GroupChat,\
GroupChatManager, UserProxyAgent, SwarmAgent, SwarmResult, AFTER_WORK, AfterWorkOption, ON_CONDITION, UPDATE_SYSTEM_MESSAGE

from teleAgent.models.agent_model.simutan_group import MyGroupManager


__CONTEXT_VARIABLES_PARAM_NAME__ = "context_variables"



async def a_initiate_swarm_chat(
    initial_agent: "SwarmAgent",
    messages: Union[List[Dict[str, Any]], str],
    agents: List["SwarmAgent"],
    user_agent: Optional[UserProxyAgent] = None,
    max_rounds: int = 20,
    context_variables: Optional[Dict[str, Any]] = None,
    after_work: Optional[Union[AFTER_WORK, Callable]] = AFTER_WORK(AfterWorkOption.TERMINATE),
) -> Tuple[ChatResult, Dict[str, Any], "SwarmAgent"]:
    """Initialize and run a swarm chat

    Args:
        initial_agent: The first receiving agent of the conversation.
        messages: Initial message(s).
        agents: List of swarm agents.
        user_agent: Optional user proxy agent for falling back to.
        max_rounds: Maximum number of conversation rounds.
        context_variables: Starting context variables.
        after_work: Method to handle conversation continuation when an agent doesn't select the next agent. If no agent is selected and no tool calls are output, we will use this method to determine the next agent.
            Must be a AFTER_WORK instance (which is a dataclass accepting a SwarmAgent, AfterWorkOption, A str (of the AfterWorkOption)) or a callable.
            AfterWorkOption:
                - TERMINATE (Default): Terminate the conversation.
                - REVERT_TO_USER : Revert to the user agent if a user agent is provided. If not provided, terminate the conversation.
                - STAY : Stay with the last speaker.

            Callable: A custom function that takes the current agent, messages, groupchat, and context_variables as arguments and returns the next agent. The function should return None to terminate.
                ```python
                def custom_afterwork_func(last_speaker: SwarmAgent, messages: List[Dict[str, Any]], groupchat: GroupChat, context_variables: Optional[Dict[str, Any]]) -> Optional[SwarmAgent]:
                ```
    Returns:
        ChatResult:     Conversations chat history.
        Dict[str, Any]: Updated Context variables.
        SwarmAgent:     Last speaker.
    """
    assert isinstance(initial_agent, SwarmAgent), "initial_agent must be a SwarmAgent"
    assert all(isinstance(agent, SwarmAgent) for agent in agents), "Agents must be a list of SwarmAgents"
    # Ensure all agents in hand-off after-works are in the passed in agents list
    for agent in agents:
        if agent.after_work is not None:
            if isinstance(agent.after_work.agent, SwarmAgent):
                assert agent.after_work.agent in agents, "Agent in hand-off must be in the agents list"

    context_variables = context_variables or {}
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    tool_execution = MySwarmAgent(
        name="Tool_Execution",
        system_message="Tool Execution",
    )
    tool_execution._set_to_tool_execution()

    # Update tool execution agent with all the functions from all the agents
    for agent in agents:
        tool_execution._function_map.update(agent._function_map)

    # Point all SwarmAgent's context variables to this function's context_variables
    # providing a single (shared) context across all SwarmAgents in the swarm
    for agent in agents + [tool_execution]:
        agent._context_variables = context_variables

    INIT_AGENT_USED = False

    def swarm_transition(last_speaker: SwarmAgent, groupchat: GroupChat):
        """Swarm transition function to determine and prepare the next agent in the conversation"""
        next_agent = determine_next_agent(last_speaker, groupchat)

        return next_agent

    def determine_next_agent(last_speaker: SwarmAgent, groupchat: GroupChat):
        """Determine the next agent in the conversation"""
        nonlocal INIT_AGENT_USED
        if not INIT_AGENT_USED:
            INIT_AGENT_USED = True
            return initial_agent

        if "tool_calls" in groupchat.messages[-1]:
            return tool_execution
        if tool_execution._next_agent is not None:
            next_agent = tool_execution._next_agent
            tool_execution._next_agent = None

            # Check for string, access agent from group chat.

            if isinstance(next_agent, str):
                if next_agent in swarm_agent_names:
                    next_agent = groupchat.agent_by_name(name=next_agent)
                else:
                    raise ValueError(
                        f"No agent found with the name '{next_agent}'. Ensure the agent exists in the swarm."
                    )

            return next_agent

        # get the last swarm agent
        last_swarm_speaker = None
        for message in reversed(groupchat.messages):
            if "name" in message and message["name"] in swarm_agent_names:
                agent = groupchat.agent_by_name(name=message["name"])
                if isinstance(agent, SwarmAgent):
                    last_swarm_speaker = agent
                    break
        if last_swarm_speaker is None:
            raise ValueError("No swarm agent found in the message history")

        # If the user last spoke, return to the agent prior
        if (user_agent and last_speaker == user_agent) or groupchat.messages[-1]["role"] == "tool":
            return last_swarm_speaker

        # No agent selected via hand-offs (tool calls)
        # Assume the work is Done
        # override if agent-level after_work is defined, else use the global after_work
        tmp_after_work = last_swarm_speaker.after_work if last_swarm_speaker.after_work is not None else after_work
        if isinstance(tmp_after_work, AFTER_WORK):
            tmp_after_work = tmp_after_work.agent

        if isinstance(tmp_after_work, SwarmAgent):
            return tmp_after_work
        elif isinstance(tmp_after_work, AfterWorkOption):
            if tmp_after_work == AfterWorkOption.TERMINATE or (
                user_agent is None and tmp_after_work == AfterWorkOption.REVERT_TO_USER
            ):
                return None
            elif tmp_after_work == AfterWorkOption.REVERT_TO_USER:
                return user_agent
            elif tmp_after_work == AfterWorkOption.STAY:
                return last_speaker
        elif isinstance(tmp_after_work, Callable):
            return tmp_after_work(last_speaker, groupchat.messages, groupchat, context_variables)
        else:
            raise ValueError("Invalid After Work condition")

    def create_nested_chats(agent: SwarmAgent, nested_chat_agents: List[SwarmAgent]):
        """Create nested chat agents and register nested chats"""
        for i, nested_chat_handoff in enumerate(agent._nested_chat_handoffs):
            nested_chats: Dict[str, Any] = nested_chat_handoff["nested_chats"]
            condition = nested_chat_handoff["condition"]

            # Create a nested chat agent specifically for this nested chat
            nested_chat_agent = SwarmAgent(name=f"nested_chat_{agent.name}_{i + 1}")

            nested_chat_agent.register_nested_chats(
                nested_chats["chat_queue"],
                reply_func_from_nested_chats=nested_chats.get("reply_func_from_nested_chats")
                or "summary_from_nested_chats",
                config=nested_chats.get("config", None),
                trigger=lambda sender: True,
                position=0,
                use_async=nested_chats.get("use_async", False),
            )

            # After the nested chat is complete, transfer back to the parent agent
            nested_chat_agent.register_hand_off(AFTER_WORK(agent=agent))

            nested_chat_agents.append(nested_chat_agent)

            # Nested chat is triggered through an agent transfer to this nested chat agent
            agent.register_hand_off(ON_CONDITION(nested_chat_agent, condition))

    nested_chat_agents = []
    for agent in agents:
        create_nested_chats(agent, nested_chat_agents)

    # Update tool execution agent with all the functions from all the agents
    for agent in agents + nested_chat_agents:
        tool_execution._function_map.update(agent._function_map)

    swarm_agent_names = [agent.name for agent in agents + nested_chat_agents]

    # If there's only one message and there's no identified swarm agent
    # Start with a user proxy agent, creating one if they haven't passed one in
    if len(messages) == 1 and "name" not in messages[0] and not user_agent:
        temp_user_proxy = [UserProxyAgent(name="_User")]
    else:
        temp_user_proxy = []

    groupchat = GroupChat(
        agents=[tool_execution]
        + agents
        + nested_chat_agents
        + ([user_agent] if user_agent is not None else temp_user_proxy),
        messages=[],  # Set to empty. We will resume the conversation with the messages
        max_round=max_rounds,
        speaker_selection_method=swarm_transition,
    )
    manager = MyGroupManager(groupchat)
    clear_history = True

    if len(messages) > 1:
        last_agent, last_message = manager.resume(messages=messages)
        clear_history = False
    else:
        last_message = messages[0]

        if "name" in last_message:
            if last_message["name"] in swarm_agent_names:
                # If there's a name in the message and it's a swarm agent, use that
                last_agent = groupchat.agent_by_name(name=last_message["name"])
            elif user_agent and last_message["name"] == user_agent.name:
                # If the user agent is passed in and is the first message
                last_agent = user_agent
            else:
                raise ValueError(f"Invalid swarm agent name in last message: {last_message['name']}")
        else:
            # No name, so we're using the user proxy to start the conversation
            if user_agent:
                last_agent = user_agent
            else:
                # If no user agent passed in, use our temporary user proxy
                last_agent = temp_user_proxy[0]

    chat_result = await last_agent.a_initiate_chat(
        manager,
        message=last_message,
        clear_history=clear_history,
    )

    # Clear the temporary user proxy's name from messages
    if len(temp_user_proxy) == 1:
        for message in chat_result.chat_history:
            if "name" in message and message["name"] == "_User":
                # delete the name key from the message
                del message["name"]

    return chat_result, context_variables, manager.last_speaker

class MySwarmAgent(SwarmAgent):
    """Swarm agent for participating in a swarm.

    SwarmAgent is a subclass of ConversableAgent.

    Additional args:
        functions (List[Callable]): A list of functions to register with the agent.
    """

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = "You are a helpful AI Assistant.",
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        functions: Union[List[Callable], Callable] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "NEVER",
        description: Optional[str] = None,
        code_execution_config=False,
        update_agent_state_before_reply: Optional[
            Union[List[Union[Callable, UPDATE_SYSTEM_MESSAGE]], Callable, UPDATE_SYSTEM_MESSAGE]
        ] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            functions=functions,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            description=description,
            code_execution_config=code_execution_config,
            update_agent_state_before_reply=update_agent_state_before_reply,
            **kwargs,
        )

   
    def _set_to_tool_execution(self):
        """Set to a special instance of SwarmAgent that is responsible for executing tool calls from other swarm agents.
        This agent will be used internally and should not be visible to the user.

        It will execute the tool calls and update the referenced context_variables and next_agent accordingly.
        """
        self._next_agent = None
        self._reply_func_list.clear()
        # self.register_reply([Agent, None], SwarmAgent.generate_swarm_tool_reply)
        self.register_reply([Agent, None], MySwarmAgent.a_generate_swarm_tool_reply)


    async def a_generate_swarm_tool_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[OpenAIWrapper] = None,
    ) -> Tuple[bool, dict]:
        """Pre-processes and generates tool call replies.

        This function:
        1. Adds context_variables back to the tool call for the function, if necessary.
        2. Generates the tool calls reply.
        3. Updates context_variables and next_agent based on the tool call response."""

        if config is None:
            config = self
        if messages is None:
            messages = self._oai_messages[sender]

        message = messages[-1]
        if "tool_calls" in message:

            tool_call_count = len(message["tool_calls"])

            # Loop through tool calls individually (so context can be updated after each function call)
            next_agent = None
            tool_responses_inner = []
            contents = []
            for index in range(tool_call_count):

                # Deep copy to ensure no changes to messages when we insert the context variables
                message_copy = copy.deepcopy(message)

                # 1. add context_variables to the tool call arguments
                tool_call = message_copy["tool_calls"][index]

                if tool_call["type"] == "function":
                    function_name = tool_call["function"]["name"]

                    # Check if this function exists in our function map
                    if function_name in self._function_map:
                        func = self._function_map[function_name]  # Get the original function

                        # Inject the context variables into the tool call if it has the parameter
                        sig = signature(func)
                        if __CONTEXT_VARIABLES_PARAM_NAME__ in sig.parameters:

                            current_args = json.loads(tool_call["function"]["arguments"])
                            current_args[__CONTEXT_VARIABLES_PARAM_NAME__] = self._context_variables
                            tool_call["function"]["arguments"] = json.dumps(current_args)

                # Ensure we are only executing the one tool at a time
                message_copy["tool_calls"] = [tool_call]

                # 2. generate tool calls reply
                _, tool_message = await self.a_generate_tool_calls_reply([message_copy])
                

                # 3. update context_variables and next_agent, convert content to string
                for tool_response in tool_message["tool_responses"]:
                    content = tool_response.get("content")
                    if isinstance(content, SwarmResult):
                        if content.context_variables != {}:
                            self._context_variables.update(content.context_variables)
                        if content.agent is not None:
                            next_agent = content.agent
                    elif isinstance(content, Agent):
                        next_agent = content

                    tool_responses_inner.append(tool_response)
                    contents.append(str(tool_response["content"]))

            self._next_agent = next_agent

            # Put the tool responses and content strings back into the response message
            # Caters for multiple tool calls
            tool_message["tool_responses"] = tool_responses_inner
            tool_message["content"] = "\n".join(contents)

            return True, tool_message
        return False, None
