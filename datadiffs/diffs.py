from collections import Callable, Sequence

from .operations import Operation
from .protocols import DEFAULT_PROTOCOL


class Diff(Sequence, Callable):

    @classmethod
    def from_serializable_data(cls, data):
        return cls(Operation.from_serializable_data(elem) for elem in data)

    def __init__(self, iterable):
        operations = tuple(iterable)
        if not all(isinstance(op, Operation) for op in operations):
            raise TypeError('iterable should countain only Operation objects')
        self.__operations = operations

    def __call__(self, value, protocol=DEFAULT_PROTOCOL):
        for op in self.__operations:
            value = op(value, protocol=protocol)
        return value

    def __getitem__(self, index):
        return self.__operations[index]

    def __len__(self):
        return len(self.__operations)

    def __iter__(self):
        return iter(self.__operations)

    def __repr__(self):
        return '{0}({1!r})'.format(
            self.__class__.__name__,
            list(self.__operations),
        )

    def inverted(self):
        return self.__class__(op.inverted()
                              for op in reversed(self.__operations))

    def to_serializable_data(self):
        return [op.to_serializable_data() for op in self.__operations]
