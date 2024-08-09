class DictTuple:
    def __init__(self, *args):
        if not args or not all(isinstance(arg, dict) for arg in args) or any(len(arg) == 0 for arg in args):
            raise AssertionError("DictTuple.__init__: All arguments must be non-empty dictionaries")
        self.dt = list(args)

    def __len__(self):
        return len(set().union(*self.dt))

    def __bool__(self):
        return len(self.dt) > 1

    def __repr__(self):
        return f"DictTuple({', '.join(repr(d) for d in self.dt)})"

    def __contains__(self, key):
        return any(key in d for d in self.dt)

    def __getitem__(self, key):
        for d in reversed(self.dt):
            if key in d:
                return d[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        if not self.dt:
            self.dt.append({})
        self.dt[-1][key] = value  # Store the value as-is, without converting to string

    def __delitem__(self, key):
        found = False
        for d in self.dt:
            if key in d:
                del d[key]
                found = True
        if not found:
            raise KeyError(key)

    def __call__(self, key):
        result = [d[key] for d in self.dt if key in d]
        if not result:
            raise KeyError(key)
        return result

    def __iter__(self):
        seen = set()
        for d in reversed(self.dt):
            for key in sorted(d.keys()):
                if key not in seen:
                    seen.add(key)
                    yield key

    def __eq__(self, other):
        if isinstance(other, DictTuple):
            return set(self) == set(other) and all(self[k] == other[k] for k in self)
        elif isinstance(other, dict):
            return set(self) == set(other) and all(self[k] == other[k] for k in self)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, DictTuple):
            return DictTuple(*(self.dt + other.dt))
        elif isinstance(other, dict):
            return DictTuple(*(self.dt + [other]))
        return NotImplemented

    def __setattr__(self, name, value):
        if hasattr(self, 'dt') and name != 'dt':
            raise AttributeError(f"Cannot add new attributes to {self.__class__.__name__}")
        super().__setattr__(name, value)

    def asdict(self):
        result = {}
        for d in reversed(self.dt):
            result.update(d)
        return result
