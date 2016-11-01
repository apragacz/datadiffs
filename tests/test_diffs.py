from hypothesis import strategies as st
from hypothesis import given

from datadiffs import Diff, find_diff


def _test_case(start_value, end_value, diff_len=None):
    diff = find_diff(start_value, end_value)
    assert isinstance(diff, Diff)
    assert diff(start_value) == end_value
    if diff_len is not None:
        assert len(diff) == diff_len
    inv_diff = diff.inverted()
    assert isinstance(inv_diff, Diff)
    assert inv_diff(end_value) == start_value
    if diff_len is not None:
        assert len(inv_diff) == diff_len


def test_cases():
    for start_value, end_value, diff_len in TEST_CASES:
        _test_case(start_value, end_value, diff_len)
        _test_case(end_value, start_value, diff_len)


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_random_lists_of_integers(l1, l2):
    _test_case(l1, l2)


@given(st.lists(st.dictionaries(st.text(), st.text())),
       st.lists(st.dictionaries(st.text(), st.text())))
def test_random_lists_of_dicts(l1, l2):
    _test_case(l1, l2)


TEST_CASES = [
    ([], [], 0),
    ({}, {}, 0),
    ('a', 'b', 1),
    ([1, 2, 3, 4, 5], [1, 10, 4, 5], 2),
    ({'a': 1, 'b': 2, 'd': 4, 'e': 5}, {'b': 3, 'c': 3, 'e': 5}, 4),
]
