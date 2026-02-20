from collections.abc import Sequence
from typing import Callable, Protocol


class Ranked(Protocol):
    rank: int


def fix_ranks[R: Ranked](
    items: Sequence[R],
    get_value: Callable[[R], int | float],
    set_rank: Callable[[R, int], None],
) -> None:
    """
    Fix the rank values of the given sequence, such that the first rank
    is 1 and the last is the count of items.  When a tie occurs, all
    candidates with that value use the same lower rank (higher numeric value).

    For example, in an election where the vote counts are [5, 5, 3],
    the tied candidates will have rank=2, and the last-place candidate rank=3.
    No candidates would have rank=1.

    Similarly, in an election where the vote counts are [5, 3, 3],
    the winner would have rank=1 while the tied candidates both have rank=3.
    No candidates would have rank=2.
    """
    last: int | float | None = None
    rank: int = len(items) + 1
    delta: int = 1
    for item in reversed(items):
        value = get_value(item)
        if value == last:
            delta += 1
        else:
            rank -= delta
            delta = 1
        set_rank(item, rank)
        last = value
