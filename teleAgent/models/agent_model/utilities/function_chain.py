from functools import partial
import inspect
import os
import traceback
from typing import Optional, List, Tuple, Union

class FunctionChain:  
    '''
    a list of functions that can be executed sequentially 
    '''
    def __init__(self, func_list: Union[List[callable], Tuple[callable]] = None ):
        self._functions = func_list if func_list else []
        self._results = {}
        self.continue_chain = True
        # TODO: add an argument wrapper
        self.args = dict()
        self.sanity_check()
        
    def sanity_check(self):
        if len(self._functions):
            sig = inspect.signature(self._functions[0])
            if not all( k in ['message', 'sender', 'recipient', 'silent'] for k in sig.parameters):
              traceback.print_exc()
              print(f'FunctionChain: the first function should have a parameter named "message"')
              __import__('ipdb').set_trace()  
        
        
    def add(self, func, index=None):
        """add a function into the chain"""
        index=len(self._functions) if index is None else index
        self._functions.insert(index, func)
        self.sanity_check()
        return self


    def execute(self, obj, *args, **kwargs):
        stop_sign = False
        return_dict = {}
        for func in self._functions:
            try:
                sig = inspect.signature(func)
                kwargs.update(self.args)
                func_kwargs = {k: v for k,v  in kwargs.items() if k in sig.parameters}
                return_dict = func( **func_kwargs)
                kwargs.update(return_dict)
                # if stop_sign: break
            except Exception as e:
                print(f'error in {func}, state: {obj.name}')
                traceback.print_exc()
                if os.getenv('DEBUG'):
                    __import__('ipdb').set_trace()
                return False, f'{e}'   

        return True, return_dict
        
    def clear(self):
        self._functions.clear()

    def stop(self):
        self.continue_chain = False

    def store_result(self, key, value):
        self._results[key] = value

    def store_dict_result(self, result_dict):
        self._results = result_dict

    def get_result(self, key, default_result=None):
        return self._results.get(key, default_result)