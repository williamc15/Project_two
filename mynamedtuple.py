from collections import OrderedDict
from keyword import kwlist


def validate_name(name: str):
    if not name:
        return False
    if not name[0].isalpha():
        return False
    if name in kwlist:
        return False
    for letter in name:
        if not letter.isdigit() and not letter.isalpha() and letter != "_":
            return False
    return True

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    if not validate_name(type_name):
        raise SyntaxError(f"Invalid Type Name: {type_name}")
    
    if isinstance(field_names, str):
        if "," in field_names:
            field_names = field_names.split(",")
        else:
            field_names = field_names.split()
    
    for field_name in field_names:
        if not validate_name(type_name):
            raise SyntaxError(f"Invalid Field Name: {field_name}")
    
    field_names = field_names = list(OrderedDict.fromkeys(field_names))
    
    defaults_keys = set(defaults.keys())

    invalid_field_names = defaults_keys.difference(set(field_names))
    
    if invalid_field_names:
        raise SyntaxError(f"Field names not found: {invalid_field_names}")
    
    args_lst=[]
    for field_name in field_names:
        if field_name not in defaults.keys():
            args_lst.append(" "+field_name)
        else:
            args_lst.append(f" {field_name}={defaults.get(field_name)}")
    
    attr_str=""
    for field_name in field_names:
        attr_str+= f"        self.{field_name} = {field_name}\n"
    
    ret_str=""
    for field_name in field_names:
        ret_str+= f"{field_name}={{self.{field_name}}},"
    ret_str=ret_str[:-1]

    accessor_str=""
    for field_name in field_names:
        accessor_str+=f"\n    def get_{field_name}(self):\n        return self.{field_name}\n"

    class_str = f"class {type_name}:\n    _fields = { field_names } \n    _mutable = { mutable }\n"
    init_str = f"\n    def __init__(self,{ ','.join(args_lst)}):\n{attr_str}"
    repr_str = f"\n    def __repr__(self):\n        return f' {{self.__class__.__name__}}({ret_str})'\n"
    get_item_str = f"\n    def __getitem__(self, index):\n        return self._fields[index]\n"
    eq_str = f"\n    def __eq__(self, coord):\n        return self.__repr__() == repr(coord)\n"
    as_dict_str = f"\n    def _asdict(self):\n        return {{field: getattr(self, field) for field in self._fields}} \n"
    make_str = f"\n    @classmethod\n    def _make(cls, values):\n        return cls(*values)\n"
    replace_str = f"\n    def _replace(self, **kargs):\n        if self._mutable:\n            for key, value in kwargs.items():\n \
               if key in self._fields:\n                    setattr(self, key, value)\n            return None \n        else:\n\
            current_values = self._asdict()\n            current_values.update(kwargs)\n \
       return self.__class__(**current_values)\n"
    setattr_str = f"\n    def __setattr__(self, name, value):\n \
        if hasattr(self, '_mutable') and not self._mutable:\n \
            raise AttributeError(f'Cannot modify {{name}}: {{self.__class__.__name__}} is immutable.')\n \
        super().__setattr__(name, value)\n"
    coord_str = class_str+init_str+repr_str+accessor_str+get_item_str+eq_str+as_dict_str+make_str+replace_str+setattr_str

    local_scope = {}
    exec(coord_str, globals(), local_scope)
    return local_scope[type_name]
