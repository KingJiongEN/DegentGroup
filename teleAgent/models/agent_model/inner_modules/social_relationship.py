from collections import defaultdict
from typing import Dict, Union, List
import random
import json

from teleAgent.models.agent_model.utilities.serialization import serializable
from teleAgent.logger.logger import shared_logger 

@serializable
class InterPersonUnderstanding:
    NECESSARY_ATTRS = ["understanding", "interaction_pattern"]
    
    def __init__(self, understanding, interaction_pattern) -> None:
        self.understanding = understanding
        self.interaction_pattern = interaction_pattern
    
    def get(self, key, default=None):
        if key == 'understanding':
            return self.understanding
        elif key == 'interaction_pattern':
            return self.interaction_pattern
        else:
            return default
    
    def update(self, data_dict):
        for key in data_dict: 
            assert hasattr(self, key)
            setattr(self, key, data_dict.get(key))    

    def to_dict(self):
        return dict( (ky, getattr(self, ky)) for ky in self.NECESSARY_ATTRS)
        return {"understanding": self.understanding,
                "interaction_pattern": self.interaction_pattern}
    
    @classmethod
    def from_dict(cls, data):
        if all( key in data for key in cls.NECESSARY_ATTRS):
            return cls(**data)
        else: 
            missing_keys = set(cls.NECESSARY_ATTRS) - set(data.keys())
            raise AssertionError(f"miss keys: {missing_keys} when instantialize {cls.__name__}")

@serializable
class SocialRelationship:
    def __init__(self, relation_list: Union[List, Dict, None] = None) -> None:
        if relation_list is None:
            self.relationship = dict()
        elif type(relation_list) is dict:
            self.relationship = relation_list
        elif type(relation_list) is list:
            self.relationship = dict( (rl.get('name'), rl ) for rl in relation_list)
        else:
            shared_logger.error(type(relation_list))
            raise NotImplemented
    
    def __repr__(self) -> str:
        return json.dumps(self.relationship, ensure_ascii=False)
    
    def impression_on_name(self, name):
        return self.relationship.get(name)
        # for rls in self.relationship: 
        #     if rls['name'] == name: # TODO duplicated name
        #         return rls
    
    def update_relationship_by_name(self,name, data_dict ):
        rls = self.impression_on_name(name)
        if rls is not None:
            rls.update(data_dict)
        else:
            self.relationship.update({name: data_dict})

    def to_dict(self):
        return {'relation_list': self.relationship}
    
    @classmethod
    def from_dict(cls, data):
        return cls(relation_list=data['relation_list'])