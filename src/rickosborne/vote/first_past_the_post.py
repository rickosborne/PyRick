from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from .candidate import Candidate
from .comparators import keyed_votes_desc_then_candidate_asc
from .fix_ranks import fix_ranks


@dataclass
class FirstPastThePostTally[C: Candidate]:
    candidate: C
    rank: int
    votes: int


@dataclass
class FirstPastThePostResult[C: Candidate]:
    ballot_count: int
    outcome: list[FirstPastThePostTally[C]]


def first_past_the_post[B, C: Candidate](
    ballots: Iterable[B], get_candidate: Callable[[B], C]
) -> FirstPastThePostResult[C]:
    """
    Tally the votes in a first-past-the-post (plurality) election.
    Tries to return the outcome by descending vote count and then
    ascending candidate.  There may be ties!

    See [First-past-the-post-voting](https://en.wikipedia.org/wiki/First-past-the-post_voting).
    """
    votes_by_candidate: dict[C, int] = {}
    ballot_count = 0
    for ballot in ballots:
        candidate = get_candidate(ballot)
        votes_by_candidate[candidate] = 1 + votes_by_candidate.get(candidate, 0)
        ballot_count += 1
    votes = [FirstPastThePostTally[C](c, 0, v) for c, v in votes_by_candidate.items()]
    votes.sort(key=keyed_votes_desc_then_candidate_asc)
    outcome: list[FirstPastThePostTally[C]] = sorted(
        votes, key=keyed_votes_desc_then_candidate_asc
    )
    fix_ranks(outcome, (lambda o: o.votes), (lambda o, r: setattr(o, "rank", r)))
    return FirstPastThePostResult(ballot_count, outcome)
