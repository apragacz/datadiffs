from .diffs import Diff
from .operations import DEFAULT_PROTOCOL, Replacement, Insertion, Deletion


SEQUENCE_TYPES = (tuple, list)


def _find_sequences_diff(old_seq, new_seq, protocol, context):
    # Simple O(n) algorithm, generating suboptimal result.
    # TODO: implement dynamic programming solution.
    old_elements = protocol.get_elements(old_seq)
    new_elements = protocol.get_elements(new_seq)
    old_lo = 0
    new_lo = 0
    old_hi = len(old_elements) - 1
    new_hi = len(new_elements) - 1
    diff = []

    changed = True
    while changed and old_lo <= old_hi and new_lo <= new_hi:
        changed = False
        if old_elements[old_lo] == new_elements[new_lo]:
            old_lo += 1
            new_lo += 1
            changed = True

            if not(old_lo <= old_hi and new_lo <= new_hi):
                break

        if old_elements[old_hi] == new_elements[new_hi]:
            old_hi -= 1
            new_hi -= 1
            changed = True

    assert old_lo == new_lo
    i = old_lo

    while i <= min(old_hi, new_hi):
        diff.extend(_find_diff(old_elements[i], new_elements[i],
                               protocol, context + (i,)))
        i += 1

    deletion_diff = []
    while i <= old_hi:
        deletion_diff.append(Deletion(
            context=context + (i,),
            old_value=old_elements[i],
        ))
        i += 1

    diff.extend(reversed(deletion_diff))

    while i <= new_hi:
        diff.append(Insertion(
            context=context + (i,),
            new_value=new_elements[i],
        ))
        i += 1

    return Diff(diff)


def _find_mapping_diff(old_mapping, new_mapping, protocol, context):
    old_dict = protocol.get_values_for_keys(old_mapping)
    new_dict = protocol.get_values_for_keys(new_mapping)
    old_keys = set(old_dict.keys())
    new_keys = set(new_dict.keys())
    diff = []

    for key in old_keys - new_keys:
        diff.append(Deletion(context=context + (key,),
                             old_value=old_dict[key]))

    for key in new_keys - old_keys:
        diff.append(Insertion(context=context + (key,),
                              new_value=new_dict[key]))

    for key in old_keys.intersection(new_keys):
        diff.extend(_find_diff(old_dict[key], new_dict[key],
                               protocol, context + (key,)))

    return Diff(diff)


def _find_diff(old_value, new_value, protocol, context):
    if old_value == new_value:
        return Diff([])

    if protocol.is_sequence(old_value) and protocol.is_sequence(new_value):
        return _find_sequences_diff(old_value, new_value, protocol, context)

    if protocol.is_mapping(old_value) and protocol.is_mapping(new_value):
        return _find_mapping_diff(old_value, new_value, protocol, context)

    return Diff([Replacement(
        context=context,
        old_value=old_value, new_value=new_value,
    )])


def find_diff(old_value, new_value, protocol=DEFAULT_PROTOCOL):
    return _find_diff(old_value, new_value, protocol, ())
