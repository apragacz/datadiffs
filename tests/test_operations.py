from datadiffs import Operation, OperationType as OT


def _test_simple_case(case):
    old_data, op_data, expected_data = case

    op = Operation.from_serializable_data(op_data)
    new_data = op(old_data)

    assert new_data is not old_data
    assert new_data == expected_data


def _test_simple_case_inverted(case):
    old_data, op_data, expected_data = case
    inv_op_data = (Operation
                   .from_serializable_data(op_data)
                   .inverted()
                   .to_serializable_data())
    _test_simple_case((expected_data, inv_op_data, old_data))


def _test_op_equality(case):
    _, op_data, _ = case
    op1 = Operation.from_serializable_data(op_data)
    op2 = Operation.from_serializable_data(op_data)
    assert op1 == op2


def test_simple_cases():
    for case in SIMPLE_TEST_CASES:
        _test_simple_case(case)
        _test_simple_case_inverted(case)
        _test_op_equality(case)


def test_eq():
    op1 = Operation.from_serializable_data({
        'type': OT.INSERTION,
        'context': ('pizzas', 1),
        'new_value': {'name': 'capriciosa'},
    })
    op2 = Operation.from_serializable_data({
        'type': OT.INSERTION,
        'context': ('pizzas',),
        'new_value': {'name': 'capriciosa'},
    })

    op3 = Operation.from_serializable_data({
        'type': OT.INSERTION,
        'context': ('pizzas', 1),
        'new_value': {'name': 'parma'},
    })
    op4 = Operation.from_serializable_data({
        'type': OT.DELETION,
        'context': ('pizzas', 1),
        'old_value': {'name': 'capriciosa'},
    })

    assert op1 != op2
    assert op2 != op3
    assert op1 != op3
    assert op1 != op4


SIMPLE_TEST_CASES = [
    (
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'hawaii'},
            ]
        },
        {
            'type': OT.INSERTION,
            'context': ('pizzas', 1),
            'new_value': {'name': 'capriciosa'},
        },
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'capriciosa'},
                {'name': 'hawaii'},
            ]
        },
    ),
    (
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'capriciosa'},
                {'name': 'hawaii'},
            ]
        },
        {
            'type': OT.DELETION,
            'context': ('pizzas', 1),
            'old_value': {'name': 'capriciosa'},
        },
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'hawaii'},
            ]
        },
    ),
    (
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'capriciosa'},
                {'name': 'hawaii'},
            ]
        },
        {
            'type': OT.REPLACEMENT,
            'context': ('pizzas', 1),
            'old_value': {'name': 'capriciosa'},
            'new_value': {'name': 'parma'},
        },
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'parma'},
                {'name': 'hawaii'},
            ]
        },
    ),
    (
        {
            'pizzas': [
                {'name': 'margarita'},
                {'name': 'parma'},
            ]
        },
        {
            'type': OT.INSERTION,
            'context': ('pizzas', 0, 'rating'),
            'new_value': 5,
        },
        {
            'pizzas': [
                {'name': 'margarita', 'rating': 5},
                {'name': 'parma'},
            ]
        },
    ),
    (
        {
            'pizzas': [
                {'name': 'margarita', 'rating': 1},
                {'name': 'parma'},
            ]
        },
        {
            'type': OT.REPLACEMENT,
            'context': ('pizzas', 0, 'rating'),
            'old_value': 1,
            'new_value': 5,
        },
        {
            'pizzas': [
                {'name': 'margarita', 'rating': 5},
                {'name': 'parma'},
            ]
        },
    ),
    (
        {},
        {
            'type': OT.INSERTION,
            'context': ('pizzas',),
            'new_value': [{'name': 'parma'}],
        },
        {
            'pizzas': [
                {'name': 'parma'},
            ]
        },
    ),
    (
        None,
        {
            'type': OT.INSERTION,
            'context': (),
            'new_value': 'foo',
        },
        'foo',
    ),
    (
        'foo',
        {
            'type': OT.REPLACEMENT,
            'context': (),
            'old_value': 'foo',
            'new_value': 'bar',
        },
        'bar',
    ),
]
