from functools import cmp_to_key
from locale import strcoll

Candidate = str | int | float


def candidate_asc(a: Candidate, b: Candidate) -> int:
    """
    Comparator for candidates, which may be text or numeric, in ascending order.
    """
    if isinstance(a, str) and isinstance(b, str):
        return strcoll(a, b)
    elif isinstance(a, int) and isinstance(b, int):
        return a - b
    elif isinstance(a, float) and isinstance(b, float):
        fdiff = a - b
        if fdiff < 0:
            return -1
        elif fdiff > 0:
            return 1
    return 0


keyed_candidate_asc = cmp_to_key(candidate_asc)
