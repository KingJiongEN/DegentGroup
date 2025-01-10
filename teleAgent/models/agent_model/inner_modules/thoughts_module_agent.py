from autogen import ConversableAgent
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent
import autogen
from teleAgent.models.agent_model.prompts.thoughts_add_prompt import ThoughtsAddPrompt
from teleAgent.models.agent_model.prompts.thoughts_solve_prompt import ThoughtsSolvePrompt
from teleAgent.models.agent_model.prompts.plan_prompt import PlanPrompt

class ThoughtsAddModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=ThoughtsAddPrompt, *args, **kwargs):
        super().__init__(
            name='thoughts_add_module',
            system_message="You are a helpful agent. Check if you feel unexpected about the updated situation.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.response_decision)
        self.function_chain.add(ThoughtsAddModuleAgent.update_thoughts)
        
  
    def response_decision(self, message_dict, recipient):
        # message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        for recordable_k in self.functional_prompt.recordable_key:
            recipient.working_memory[recordable_k] = message_dict[recordable_k] 
        if True: #message_dict['unexpected_level'] > 5:
            steps2add = []
            for next_step in message_dict['next_steps']:
                if next_step['does_similar_thoughts_exist'] == 'no':
                    steps2add.append({"thought":f"@{next_step['act_object']}, {next_step['thought_to_do']}",
                                                           "act_channel": next_step['channel']})
            self.logger.info(f"{recipient.name} steps2add: {steps2add}")
            return {"next_step":  steps2add}
        else:
            return {"next_step":  f"null" }
    
    @staticmethod
    def update_thoughts(next_step, recipient):
        if next_step != 'null':
            recipient.thoughts.add_quick_thoughts(next_step)
        return dict()

class ThoughtsSolveModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=ThoughtsSolvePrompt, *args, **kwargs):
        super().__init__(
            name='thoughts_solve_module',
            system_message="You are a helpful agent. Check if your previous thoughts have been sovled.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.response_decision)
        self.function_chain.add(ThoughtsSolveModuleAgent.update_thoughts)
        
  
    def response_decision(self, message_dict, recipient):
        # message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        self.logger.info(f"{recipient.name}  remove thoughts: {message_dict}")
        return {"thought_to_remove": message_dict['thought_to_remove_list'], "next_steps": message_dict['next_steps'] }
    
    @staticmethod
    def update_thoughts(thought_to_remove, next_steps, recipient):
        recipient.thoughts.remove_quick_thought(thought_to_remove)
        recipient.thoughts.add_quick_thoughts(next_steps)
        return {"message": str({'next_steps': next_steps})}
    
class PlanDetailModuleAgent(CognitiveModuleAgent):
    """
    This module adds expectations to quick thoughts
    Maybe not so necessary.
    """
    def __init__(self, function_prompt=PlanPrompt, *args, **kwargs):
        super().__init__(
            name='plan_detail_module',
            system_message="You are a helpful agent. Check if your previous thoughts have been sovled.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.response_decision)
        # self.function_chain.add(ThoughtsSolveModuleAgent.update_thougts)

    def add_expectations(self, message_dict, recipient):
        for thought_exp_dict in message_dict['thought_expectations']:
            recipient.add_expectation(
                {
                    thought_exp_dict['thought_to_do']: thought_exp_dict['expect_reeults']
                }
            )
        return dict()
        