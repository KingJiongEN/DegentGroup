import json
from functools import wraps

class SerializationRegistry:
    _registry = {}

    @classmethod
    def register_class(cls, class_type):
        cls._registry[class_type.__name__] = {
            'to_dict': class_type.to_dict,
            'from_dict': class_type.from_dict,
            'class': class_type
        }

    @classmethod
    def get_to_dict_method(cls, class_type):
        return cls._registry[class_type.__name__]['to_dict']

    @classmethod
    def get_from_dict_method(cls, class_name):
        return cls._registry[class_name]['from_dict']

    @classmethod
    def get_class(cls, class_name):
        return cls._registry[class_name]['class']

def serializable(cls):
    SerializationRegistry.register_class(cls)
    return cls

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        class_name = obj.__class__.__name__
        if class_name in SerializationRegistry._registry:
            to_dict_method = SerializationRegistry.get_to_dict_method(obj.__class__)
            return {'__class__': class_name, '__data__': to_dict_method(obj)}
        return super().default(obj)

def custom_json_decoder(dct):
        if '__class__' in dct and '__data__' in dct:
            class_name = dct['__class__']
            data = dct['__data__']
            from_dict_method = SerializationRegistry.get_from_dict_method(class_name)
            return from_dict_method(data)
        return dct

if __name__ == '__main__':
    @serializable
    class MyClass:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def to_dict(self):
            return {
                'a': self.a,
                'b': self.b,
                'c': self.c
            }

        @classmethod
        def from_dict(cls, data):
            return cls(data['a'], data['b'], data['c'])
    

    # Example usage
    obj = MyClass(1, 2, 3)

    # Serialize the object to JSON
    serialized_obj = json.dumps(obj, cls=CustomJSONEncoder, ensure_ascii=False)

    # Deserialize the JSON back to an object
    deserialized_obj = json.loads(serialized_obj, object_hook=custom_json_decoder)

    print(deserialized_obj.a, deserialized_obj.b, deserialized_obj.c)  # Output: 1 2 3
