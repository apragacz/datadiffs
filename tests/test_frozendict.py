import pytest
from datadiffs.freezing import frozendict


def test_not_implemented():
    fd = frozendict({'a': 1})
    with pytest.raises(NotImplementedError):
        fd.setdefault('a', 2)
    with pytest.raises(NotImplementedError):
        fd.clear()
    with pytest.raises(NotImplementedError):
        fd['b'] = 3


def test_copy():
    fd1 = frozendict({'a': 1})
    fd2 = fd1.copy()
    assert fd1 is not fd2
    assert fd1 == fd2
    assert isinstance(fd2, frozendict)


def test_pop():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2, v = fd1.pop('a')
    assert fd1 == frozendict({'a': 1, 'b': 3})
    assert fd2 == frozendict({'b': 3})
    assert v == 1


def test_popitem():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2, item = fd1.popitem()
    assert fd1 == frozendict({'a': 1, 'b': 3})
    assert len(fd2) == len(fd1) - 1
    assert item in (('a', 1), ('b', 3))


def test_update():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2 = fd1.update({'b': 2, 'c': 4})
    assert fd1 == frozendict({'a': 1, 'b': 3})
    assert fd2 == frozendict({'a': 1, 'b': 2, 'c': 4})


def test_hash():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2 = frozendict({'a': 1, 'b': 3})
    assert hash(fd1) == hash(fd2)


def test_repr():
    fd = frozendict({'a': 1, 'b': 3})
    assert repr(fd).startswith('frozendict')
