'''
This module decides if the agent need to response to the group chat or just wait. 
'''

from autogen import ConversableAgent
from teleAgent.models.agent_model.inner_modules.module_agent import CognitiveModuleAgent
import autogen
from teleAgent.models.agent_model.prompts.reflect_people_prompt import ReflectPeoplePrompt
from teleAgent.models.agent_model.prompts.reflect_interaction_prompt import ReflectInteractionPrompt

class ReflectPeopleModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=ReflectPeoplePrompt, *args, **kwargs):
        super().__init__(
            name='reflect_people_module',
            system_message="You are a helpful people.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.update_understanding)
        
  
    def update_understanding(self, message_dict, recipient):
        # message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        understanding_updated = []
        for dic in message_dict['reflections']:
            if dic['unexpected_observation'] != 'null' :
                # for recordable_k in self.functional_prompt.recordable_key:
                #     recipient.working_memory[recordable_k] = dic[recordable_k] 
                    # self.logger.info(f"{recordable_k}: {dic[recordable_k]}")        
                if 'unexpectation_level' not in dic: self.logger.info(f"unexpectation_level not in dic: {dic}")
                if dic['unexpectation_level'] >6 and  dic['explanatory_power_new'] > dic['explanatory_power_prev'] :
                    reflect_object = dic['reflect_object'] 
                    recipient.social_relations.update_relationship_by_name(reflect_object, {"understanding": dic['new_understanding']} ) 
                    self.logger.info(f"{recipient.name} is reflecting on {reflect_object}")
                    self.logger.info(f"reflection people: {dic}")
                    self.logger.info(recipient.social_relations.impression_on_name(reflect_object))
                    understanding_updated.append(dic)
        
        if understanding_updated:
            return {'message': str(understanding_updated)}
        else: 
            return {'message': """no new understanding of people""" }
        
    
class ReflectInteractionModuleAgent(CognitiveModuleAgent):
    def __init__(self, function_prompt=ReflectInteractionPrompt, *args, **kwargs):
        super().__init__(
            name='reflect_interaction_module',
            system_message="You are a helpful people.",
            functional_prompt=function_prompt,
            *args, **kwargs)
        self.function_chain.add(self.update_understanding)
        
  
    def update_understanding(self, message_dict, recipient: "ProactGroupAgent"):
        # message_dict = eval(self.functional_prompt.extract_json_from_markdown(message))
        understanding_updated = []
        for dic in message_dict['reflections']: 
            if dic['new_understanding'] != 'null' :
                # for recordable_k in self.functional_prompt.recordable_key:
                    # recipient.working_memory[recordable_k] = dic[recordable_k] 
                    # self.logger.info(f"{recordable_k}: {dic[recordable_k]}")        
                self.logger.info(f"reflection interaction: {dic}")
                reflect_object = dic['reflect_object'] 
                recipient.social_relations.update_relationship_by_name(reflect_object, {"interaction_pattern": dic['new_interaction_pattern']} ) 
                self.logger.info(recipient.social_relations.impression_on_name(reflect_object))
                understanding_updated.append(dic)
                
        if understanding_updated:
            return {'message': str(understanding_updated)}
        else:
            return {'message': """no new interaction pattern of others""" }