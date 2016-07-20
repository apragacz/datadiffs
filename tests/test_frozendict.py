from datadiffs.freezing import frozendict


def test_getitem():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert fd1['a'] == 1
    assert fd1['b'] == 3


def test_len():
    fd0 = frozendict({})
    fd1 = frozendict({'a': 1, 'b': 3})
    assert len(fd0) == 0
    assert not bool(fd0)
    assert len(fd1) == 2
    assert bool(fd1)


def test_iter():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert set(fd1) == {'a', 'b'}


def test_contains():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert 'a' in fd1
    assert 'b' in fd1
    assert 'c' not in fd1


def test_hash():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2 = frozendict({'a': 1, 'b': 3})
    assert hash(fd1) == hash(fd2)


def test_repr():
    fd = frozendict({'a': 1, 'b': 3})
    assert repr(fd).startswith('frozendict')


def test_items():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert sorted(fd1.items()) == [('a', 1), ('b', 3)]


def test_keys():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert set(fd1.keys()) == {'a', 'b'}


def test_values():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert sorted(fd1.values()) == [1, 3]


def test_get():
    fd1 = frozendict({'a': 1, 'b': 3})
    assert fd1.get('a', 4) == 1
    assert fd1.get('b', 4) == 3
    assert fd1.get('c', 4) == 4
    assert fd1.get('a') == 1
    assert fd1.get('b') == 3
    assert fd1.get('c') is None


def test_put():
    fd1 = frozendict({'a': 1, 'b': 3})
    fd2 = fd1.put('a', 2)
    fd3 = fd1.put('c', 2)
    assert fd1 != fd2
    assert fd1 != fd3
    assert fd1 == frozendict({'a': 1, 'b': 3})
    assert fd2 == frozendict({'a': 2, 'b': 3})
    assert fd3 == frozendict({'a': 1, 'b': 3, 'c': 2})


def test_delete():
    fd1 = frozendict({'a': 1})
    fd2 = fd1.delete('a')
    assert fd1 != fd2
    assert fd2 == frozendict({})


def test_copy():
    fd1 = frozendict({'a': 1})
    fd2 = fd1.copy()
    assert fd1 is not fd2
    assert fd1 == fd2
    assert isinstance(fd2, frozendict)
