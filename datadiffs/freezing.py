

class frozendict(dict):

    def __hash__(self):
        h = 0
        for item in self.items():
            h += hash(item)
        return h

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, super().copy())

    def copy(self):
        return frozendict(super().copy())

    def pop(self, *args, **kwargs):
        d = super().copy()
        v = d.pop(*args, **kwargs)
        return frozendict(d), v

    def popitem(self, *args, **kwargs):
        d = super().copy()
        item = d.popitem(*args, **kwargs)
        return frozendict(d), item

    def update(self, E, **F):
        d = super().copy()
        d.update(E, **F)
        return frozendict(d)

    def clear(self):
        raise NotImplementedError()

    def setdefault(self, k, d):
        raise NotImplementedError()


def freeze_data(data):
    if isinstance(data, (dict, frozendict)):
        return frozendict({k: freeze_data(v) for k, v in data.items()})
    elif isinstance(data, (tuple, list)):
        return tuple(freeze_data(el) for el in data)
    else:
        return data


def unfreeze_data(data):
    if isinstance(data, (dict, frozendict)):
        return {k: unfreeze_data(v) for k, v in data.items()}
    elif isinstance(data, (tuple, list)):
        return [unfreeze_data(el) for el in data]
    else:
        return data
