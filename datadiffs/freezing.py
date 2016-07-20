from collections import Mapping


class frozendict(Mapping):

    def __init__(self, input):
        if not isinstance(input, dict):
            raise TypeError('{0} is not type of dict'.format(type(input)))
        self.__dict = input.copy()

    def __getitem__(self, key):
        return self.__dict[key]

    def __len__(self):
        return len(self.__dict)

    def __iter__(self):
        return iter(self.__dict)

    def __contains__(self, item):
        return item in self.__dict

    def __hash__(self):
        h = 0
        for item in self.__dict.items():
            h += hash(item)
        return h

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.__dict)

    def items(self):
        return self.__dict.items()

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def get(self, key, default=None):
        return self.__dict.get(key, default)

    def put(self, key, value):
        copy = self.__dict.copy()
        copy[key] = value
        return self.__class__(copy)

    def delete(self, key):
        copy = self.__dict.copy()
        del copy[key]
        return self.__class__(copy)

    def copy(self):
        return self.__class__(self.__dict.copy())


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
