from functools import cmp_to_key
from typing import Protocol

from .candidate import Candidate, candidate_asc


class HasVotes(Protocol):
    candidate: Candidate
    votes: int


def votes_desc_then_candidate_asc[HV: HasVotes](a: HV, b: HV) -> int:
    """
    Comparator for structures which have candidates and votes.
    Orders by vote count descending, then candidate ascending.
    """
    diff = b.votes - a.votes
    return diff if diff != 0 else candidate_asc(a.candidate, b.candidate)


keyed_votes_desc_then_candidate_asc = cmp_to_key(votes_desc_then_candidate_asc)
