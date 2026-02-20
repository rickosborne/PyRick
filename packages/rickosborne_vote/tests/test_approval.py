from rickosborne_vote.approval import ApprovalResult, ApprovalResultOutcome, approval


def test_empty():
    actual = approval([], lambda b: "")
    expected = ApprovalResult[str]([])
    assert actual == expected


def test_tie():
    ballots = [
        ["A", "B"],
        ["A", "C"],
        ["B", "C"],
    ]
    actual = approval(ballots, lambda b: b)
    expected = ApprovalResult(
        [
            ApprovalResultOutcome("A", 3, 2),
            ApprovalResultOutcome("B", 3, 2),
            ApprovalResultOutcome("C", 3, 2),
        ]
    )
    assert actual == expected


def test_no_ties():
    ballots = [
        ["A", "B", "C"],
        ["A", "C"],
        ["B", "C"],
        ["B"],
        ["C"],
    ]
    actual = approval(ballots, lambda b: b)
    expected = ApprovalResult(
        [
            ApprovalResultOutcome("C", 1, 4),
            ApprovalResultOutcome("B", 2, 3),
            ApprovalResultOutcome("A", 3, 2),
        ]
    )
    assert actual == expected
