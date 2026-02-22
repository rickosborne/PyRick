from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from .candidate import Candidate
from .comparators import keyed_votes_desc_then_candidate_asc
from .fix_ranks import fix_ranks


@dataclass
class ApprovalResultOutcome[C: Candidate]:
    candidate: C
    rank: int
    votes: int


@dataclass
class ApprovalResult[C: Candidate]:
    outcome: list[ApprovalResultOutcome[C]]


def approval[B, C: Candidate](
    ballots: Iterable[B],
    get_approved: Callable[[B], Iterable[C]],
) -> ApprovalResult[C]:
    """
    Tally the votes in an Approval election.
    Tries to return the outcome by descending vote count and then
    ascending candidate.  There may be ties!

    See [Approval voting](https://en.wikipedia.org/wiki/Approval_voting).
    """
    totals = dict[C, int]()
    for ballot in ballots:
        candidates = get_approved(ballot)
        for candidate in candidates:
            totals[candidate] = 1 + totals.get(candidate, 0)
    outcome = [ApprovalResultOutcome[C](c, 0, v) for c, v in totals.items()]
    outcome.sort(key=keyed_votes_desc_then_candidate_asc)
    fix_ranks(outcome, (lambda o: o.votes), (lambda o, r: setattr(o, "rank", r)))
    return ApprovalResult[C](outcome)
