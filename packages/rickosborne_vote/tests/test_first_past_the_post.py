from rickosborne_vote.first_past_the_post import (
    FirstPastThePostResult,
    FirstPastThePostTally,
    first_past_the_post,
)


def test_empty():
    actual = first_past_the_post([], lambda b: "")
    expected = FirstPastThePostResult[str](0, [])
    assert actual == expected


def test_clear_winner():
    ballots = ["A", "B", "A", "A", "B", "B", "Q", "B"]
    actual = first_past_the_post(ballots, (lambda b: b))
    expected = FirstPastThePostResult(
        8,
        [
            FirstPastThePostTally("B", 1, 4),
            FirstPastThePostTally("A", 2, 3),
            FirstPastThePostTally("Q", 3, 1),
        ],
    )
    assert actual == expected


def test_ties():
    ballots = ["A", "B", "A", "B", "D", "C", "E"]
    actual = first_past_the_post(ballots, (lambda b: b))
    expected = FirstPastThePostResult(
        7,
        [
            FirstPastThePostTally("A", 2, 2),
            FirstPastThePostTally("B", 2, 2),
            FirstPastThePostTally("C", 5, 1),
            FirstPastThePostTally("D", 5, 1),
            FirstPastThePostTally("E", 5, 1),
        ],
    )
    assert actual == expected
