import keyword
from collections import OrderedDict

from keyword import kwlist


def validate_name(name: str):
    name=str(name)
    name=name.strip()
    print(f"'{name}'")
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
    # Validate type_name
    if not validate_name(type_name):
        raise SyntaxError(f"Invalid type name: {type_name}")

    # Process field_names
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(OrderedDict.fromkeys(field_names))  # Remove duplicates while preserving order

    # Validate field_names
    for name in field_names:
        if not validate_name(name):
            raise SyntaxError(f"Invalid field name: {name}")

    # Validate defaults
    for key in defaults:
        if key not in field_names:
            raise SyntaxError(f"Default provided for non-existent field: {key}")

    # Generate the class string
    class_definition = f"class {type_name}:\n"
    class_definition += f"    _fields = {field_names}\n"
    class_definition += f"    _mutable = {mutable}\n\n"

    # __init__ method
    init_params = ', '.join([f"{name}={defaults.get(name, 'None')}" for name in field_names])
    class_definition += f"    def __init__(self, {init_params}):\n"
    for name in field_names:
        class_definition += f"        self.{name} = {name}\n"
    class_definition += "\n"

    # __repr__ method
    class_definition += "    def __repr__(self):\n"
    repr_str = f"{type_name}(" + ",".join([f"{name}={{self.{name}!r}}" for name in field_names]) + ")"
    class_definition += f"        return f'{repr_str}'\n\n"

    # Getter methods
    for name in field_names:
        class_definition += f"    def get_{name}(self):\n"
        class_definition += f"        return self.{name}\n\n"

    # __getitem__ method
    class_definition += "    def __getitem__(self, index):\n"
    class_definition += "        return getattr(self, self._fields[index])\n\n"

    # __eq__ method
    class_definition += "    def __eq__(self, other):\n"
    class_definition += "        if not isinstance(other, self.__class__):\n"
    class_definition += "            return NotImplemented\n"
    class_definition += "        return all(getattr(self, name) == getattr(other, name) for name in self._fields)\n\n"

    # asdict method
    class_definition += "    def _asdict(self):\n"
    class_definition += "        return {name: getattr(self, name) for name in self._fields}\n\n"

    # make method
    class_definition += "    @classmethod\n"
    class_definition += "    def _make(cls, iterable):\n"
    class_definition += "        return cls(*iterable)\n\n"

    # replace method
    class_definition += "    def _replace(self, **kwargs):\n"
    class_definition += "        if self._mutable:\n"
    class_definition += "            for name, value in kwargs.items():\n"
    class_definition += "                if name not in self._fields:\n"
    class_definition += "                    raise TypeError('invalid value')\n"
    class_definition += "                setattr(self, name, value)\n"
    class_definition += "        else:\n"
    class_definition += "            new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n"
    class_definition += "            return self.__class__(**new_values)\n\n"

    # __setattr__ method
    class_definition += "    def __setattr__(self, name, value):\n"
    class_definition += "        if not self._mutable and name in self._fields and hasattr(self, name):\n"
    class_definition += "            raise AttributeError(f'Cannot modify immutable {self.__class__.__name__}')\n"
    class_definition += "        super().__setattr__(name, value)\n"

    # Create and return the class object
    namespace = {}
    exec(class_definition, namespace)
    return namespace[type_name]
