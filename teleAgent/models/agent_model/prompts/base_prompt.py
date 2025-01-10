import copy
import json
import os
import re
import traceback
from typing import List, Optional, Union

from teleAgent.logger.logger import shared_logger

class BasePrompt:

    PROMPT = '''
    '''
    
    def __init__(self, prompt_type, check_exempt_layers=[2,3,4,5,6,7,8,9]) -> None:
        '''
        recordable_key: store the value of this key from the llm response to character.working_memory
        warning_message: warning to be add across different callings
        '''
        self.prompt_type = prompt_type
        # self.character:Character = state.character
        # self.character_list: CharacterList = state.character_list
        # self.building_list: BuildingList = state.building_list
        # self.followed_state_format = '({sid}) {state_des}: {state_requirments}\n\n'
        self.entire_prompt_format = '{PROMPT}\n\n Please decide what to do next and return the json dict from the following options\n\n{followed_states_text}'
        self.waring_message = ['Warning: in previous attempts, the returned response met the following errors:\n'] 
        self.warning_added = False
        self.check_exempt_layers = check_exempt_layers
        self.error_seperator = '###'
         
        self.recordable_key = None 
    
    def set_recordable_key(self, key: Union[str, List[str]]):
        if type(key) is str : 
            self.recordable_key = [key]
        elif type(key) is list:
            assert all([ type(ky) is str for ky in key]), f' all elements in keys list should be str, current key is {key}'
            self.recordable_key = key
        else:
            raise NotImplemented
        
    def __call__(self):
        return self.format_attr()
   
    def add_warning_msg(self, warning_message):
        self.warning_added += 1
        if self.warning_added > 3: # limit the length of warning message
           self.waring_message.remove(self.waring_message[1]) 
        self.waring_message.append(warning_message + '\n')
        
    def format_attr(self, 
                    **kwargs,
                    ) -> str:
       
        # replace placeholder with character info and building list
        # return prompt
        
        base_prompt = self.PROMPT
        
        att_dict = dict()
        # att_dict.update({'memory': self.character.longterm_memory.to_json()})
        # att_dict.update(self.character.working_memory.serialize())
        att_dict.update(kwargs)
        
        attributes = re.findall(r'\{([a-zA-Z_]+)\}', base_prompt)
        for att in attributes:
            if att in att_dict:
                att_val = att_dict[att]
            elif hasattr(self, att):
                att_val = getattr(self, att)
            # elif hasattr(self.character, att):
            #     att_val = getattr(self.character, att)
            # elif att in self.character.working_memory.wm: # TODO
            #     att_val = self.character.working_memory.get(att)   
            else:
                raise  AssertionError(f'Missing attribute: {att} . Current prompt: {self.prompt_type}')
            try:
                base_prompt = base_prompt.replace('{'+att+'}', str(att_val))
            except:
                traceback.print_exc()
                if os.getenv('DEBUG'):
                    __import__('ipdb').set_trace()
                pass        
        
        
        base_prompt = base_prompt.replace('TERMINATE','') # in case that interaction history has 'TERMINATE'. TODO: make it more elegant
        if self.warning_added:
            base_prompt = base_prompt + ' '.join(self.waring_message)
        return base_prompt
        
     
    def response_format_check(self, response, check_exempt_layers):
        try:
            response_dict = BasePrompt.response_json_check(response)
            self.response_structure_check(response_dict,check_exempt_layers)
        except Exception as e:
            return f'{self.error_seperator} Please NOTICE that {e} '
        
    @staticmethod
    def response_json_check(response):
        response = BasePrompt.extract_json_from_markdown(response)
        try:        
            if type(response) not in [dict, list]:
                response = eval(response) 
        except:
            try:
                response = json.loads(response) 
            except:           
                # __import__('ipdb').set_trace()
                shared_logger.erro(f'Can not load reply as json, reply: {response}')
                raise AssertionError('Must return a json ')
        
        return response
    
    @staticmethod
    def extract_json_from_markdown(markdown_text):
        # Regular expression to match the content inside ```json``` tags
        pattern = r'```json\n(.*?)```'
        # Find all matches
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        # If there are matches, return the first one
        if matches:
            # Remove leading and trailing whitespace and newlines
            json_content = matches[0].strip()
            return json_content
        else:
            return markdown_text
        
    def response_structure_check(self, response_dict, exempt_layers=[2,3,4,5,6,7,8,9,10]):    
        if hasattr(self, 'EXAMPLE'):
            prompt_example = self.EXAMPLE if type(self.EXAMPLE) in [dict,list] else json.loads(self.EXAMPLE)
            self.have_same_structure(prompt_example, response_dict, exempt_layers=exempt_layers)
            
    def have_same_structure(self, ground_turth_dict, pred_dict, layer=0, exempt_layers=[2,3,4,5,6,7,8,9,10]): 
        '''
        eval if the return dict and sample dict have the same hierarchical structure
        in default, only the 0,1 layer is checked
        '''
        if isinstance(ground_turth_dict, dict) and isinstance(pred_dict, dict):
            # Check if both dictionaries have the same set of keys
            # if set(ground_turth_dict.keys()) != set(pred_dict.keys()) and (layer not in exempt_layers):
                # raise AssertionError(f'dict keys should be strictly conformed to {list(ground_turth_dict.keys())}')
            if ( set(ground_turth_dict.keys()) - set(pred_dict.keys())) and (layer not in exempt_layers):
                raise AssertionError(f'dict keys must contain all the following: {list(ground_turth_dict.keys())}')
            
            # Recursively check the structure of each key-value pair
            if layer not in exempt_layers:
                for key in ground_turth_dict:
                    self.have_same_structure(ground_turth_dict[key], pred_dict[key], layer=layer+1, exempt_layers=exempt_layers)
            # else:
            #     # assume the order of values does not matter
            #     for g_v, p_v in zip(ground_turth_dict.values(), pred_dict.values()):
            #         self.have_same_structure(g_v, p_v, layer=layer+1, exempt_layers=exempt_layers)

        # If either of the values is not a dictionary, treat as leaf node
        assert type(ground_turth_dict) == type(pred_dict), f'the type of {pred_dict} should be {type(ground_turth_dict)}'
    