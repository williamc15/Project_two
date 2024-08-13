class DictTuple:
    def __init__(self,dt: list) -> None:
        if not dt or not isinstance(dt, list):
            raise AssertionError(f"{self.__class__.__name__}.init : {dt} is not a list of dictionaries")
        for d in dt:
            if not isinstance(d, dict):
                raise AssertionError(f"{self.__class__.__name__}.init : {d} is not a dictionary")
        self.dt = dt
    
    def __len__(self):
        keys=[]
        for d in self.dt:
            keys.extend(d.keys())
        return len(set(keys))

    def __bool__(self):
        return self.__len__() > 1
    
    def __repr__(self):
        dict_reprs = []
        for d in self.dt:
            items_repr = ', '.join(f'{repr(k)}: {repr(v)}' for k, v in d.items())
            dict_reprs.append(f'{{{items_repr}}}')
        return f"{self.__class__.__name__}({', '.join(dict_reprs)})"
    
    def __contains__(self, key):
        for d in self.dt:
            if key in d:
                return True
        return False
    
    def __getitem__(self, key):
        for d in reversed(self.dt):
            if key in d:
                return d[key]
        raise KeyError(f"Key '{key}' not found in any of the data types.")
    
    def __setitem__(self, key, value):
        for i in range(len(self.dt) - 1, -1, -1):
            if key in self.dt[i]:
                self.dt[i][key] = value
                return
        self.dt.append({key: value})
    
    def __delitem__(self, key):
        key_found = False
        for d in self.dt:
            if key in d:
                key_found = True
                del d[key]
        
        if not key_found:
            raise KeyError(f"Key '{key}' not found in any of the data types.")
    
    def __call__(self, key):
        result = []
        for d in self.dt:
            if key in d:
                result.append(d[key])
        return result
    
    def __iter__(self):
        seen_keys = set()
        keys = []
        for d in reversed(self.dt):
            for key in d:
                if key not in seen_keys:
                    seen_keys.add(key)
                    keys.append(key)
    
        keys.sort()
        for key in keys:
            yield key
    
    def __eq__(self, other_dt):
        if isinstance(other_dt, DictTuple):
            for key in self:
                if key not in other_dt:
                    return False
                if self[key] != other_dt[key]:
                    return False
            for key in other_dt:
                if key not in self:
                    return False
                if other_dt[key] != self[key]:
                    return False
            return True

        elif isinstance(other_dt, dict):
            for key in self:
                if key not in other_dt:
                    return False
                if self[key] != other_dt[key]:
                    return False
            return True

        return False
    def __add__(self, other_dt):
        if isinstance(other_dt, DictTuple):
            return DictTuple(self.dt + other_dt.dt)
        
        elif isinstance(other_dt, dict):
            return DictTuple(self.dt + [other_dt])
        
        elif isinstance(other_dt, DictTuple):
            return DictTuple([other_dt] + self.dt)
        
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'DictTuple' and '{type(other_dt).__name__}'")
        
    def __setattr__(self, name, value):
        if name in {'dt'}:
            super().__setattr__(name, value)
        else:
            raise AssertionError(f"Cannot add or modify attribute '{name}' in {self.__class__.__name__}")
