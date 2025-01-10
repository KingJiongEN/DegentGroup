from teleAgent.models.agent_model.utilities.serialization import serializable

@serializable
class Plan:
    '''
    quick thoughts are what to do next, a list like [ {"thought": "@someone, do something","act_channel": private/public} , {"thought":...,"act_channel":...}]
    plans = quick thoughts + expectations
    public/private_chat_thoughts are list of public/private thoughts
    '''
    def __init__(self, quick_thoughts=None, public_chat_thoughts=None, private_chat_thoughts=None, max_quick_thoughts=4) -> None:
        self.quick_thoughts = []
        self.plans = {}
        self.public_chat_thoughts = []
        self.private_chat_thoughts = []
        self.max_quick_thoughts = max_quick_thoughts
        
        if quick_thoughts is not None:
            self.add_quick_thoughts(quick_thoughts)
        elif public_chat_thoughts is not None or private_chat_thoughts is not None:
            self.build_from_chat_thoughts(public_chat_thoughts, private_chat_thoughts)
    
    def add_quick_thoughts(self, thoughts):
        if isinstance(thoughts, str):
            self._add_single_thought({"thought": thoughts, "act_channel": "public"})
        elif isinstance(thoughts, list):
            for thought in thoughts:
                if isinstance(thought, str):
                    self._add_single_thought({"thought": thought, "act_channel": "public"})
                elif isinstance(thought, dict):
                    self._add_single_thought(thought)
                else:
                    raise ValueError("Unsupported type for thought in list")
        elif isinstance(thoughts, dict):
            self._add_single_thought(thoughts)
        else:
            raise ValueError("Unsupported type for thoughts")

    def _add_single_thought(self, thought):
        self._add_single_thought_to_list(thought, self.quick_thoughts)
        channel = thought.get('act_channel')
        if channel and channel == 'public':
            self._add_single_thought_to_list(thought.get('thought'), self.public_chat_thoughts)
        elif channel and channel == 'private':
            self._add_single_thought_to_list(thought.get('thought'), self.private_chat_thoughts)
         
    def _add_single_thought_to_list(self, thought, thought_list):
        if len(thought_list) < self.max_quick_thoughts:
            thought_list.append(thought)
        else:
            thought_list.pop(0)  # Remove the oldest thought
            thought_list.append(thought)    
    
    def remove_quick_thought(self, thoughts):
        assert isinstance(thoughts, list)
        self.quick_thoughts = [t for t in self.quick_thoughts if t not in thoughts]
   
    def thoughts_about_object(self, object_name):
        return self.private_chat_thoughts_about_object(object_name) + self.public_chat_thoughts_about_object(object_name)
   
    def private_chat_thoughts_about_object(self, object_name):
        return [t for t in self.private_chat_thoughts if object_name in t]
   
    def public_chat_thoughts_about_object(self, object_name):
        return [t for t in self.public_chat_thoughts if object_name in t]
   
    def add_expectation(self, thought, expectations):
        self.plans.update({thought: list(expectations)})
        
    def build_from_chat_thoughts(self, public_chat_thoughts=None, private_chat_thoughts=None):
        if public_chat_thoughts:
            for thought in public_chat_thoughts:
                self._add_single_thought({"thought": thought, "act_channel": "public"})
        if private_chat_thoughts:
            for thought in private_chat_thoughts:
                self._add_single_thought({"thought": thought, "act_channel": "private"})
    
    @classmethod
    def from_quick_thoughts(cls, quick_thoughts, max_quick_thoughts=5):
        return cls(quick_thoughts=quick_thoughts, max_quick_thoughts=max_quick_thoughts)
    
    @classmethod
    def from_chat_thoughts(cls, public_chat_thoughts=None, private_chat_thoughts=None, max_quick_thoughts=5):
        plan = cls(max_quick_thoughts=max_quick_thoughts)
        plan.build_from_chat_thoughts(public_chat_thoughts, private_chat_thoughts)
        return plan
    
    def __repr__(self) -> str:
        return f"thoughts to do in public: {self.public_chat_thoughts}, thoughts to do in private: {self.private_chat_thoughts}"
    
    def to_dict(self):
        return {
            "quick_thoughts": self.quick_thoughts,
            "public_chat_thoughts": self.public_chat_thoughts,
            "private_chat_thoughts": self.private_chat_thoughts,
            "max_quick_thoughts": self.max_quick_thoughts
        }
    
    @classmethod
    def from_dict(cls, data):
        plan = cls(max_quick_thoughts=data.get('max_quick_thoughts', 5))
        plan.quick_thoughts = data.get('quick_thoughts', [])
        plan.public_chat_thoughts = data.get('public_chat_thoughts', [])
        plan.private_chat_thoughts = data.get('private_chat_thoughts', [])
        return plan