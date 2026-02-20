from rickosborne_vote.candidate import keyed_candidate_asc


def test_text():
    names = ["B", "Q", "Ab", "Ac"]
    actual = sorted(names, key=keyed_candidate_asc)
    expected = ["Ab", "Ac", "B", "Q"]
    assert actual == expected


def test_int():
    names = [5, 4, 3, 7]
    actual = sorted(names, key=keyed_candidate_asc)
    expected = [3, 4, 5, 7]
    assert actual == expected


def test_float():
    names = [5.1, 4.3, 4.2, 7.0]
    actual = sorted(names, key=keyed_candidate_asc)
    expected = [4.2, 4.3, 5.1, 7.0]
    assert actual == expected


def test_mixed():
    """
    Instead of throwing, the function just leaves items
    where they are if they can't be compared.
    """
    names = ["a", 1, 1.1]
    actual = sorted(names, key=keyed_candidate_asc)
    expected = ["a", 1, 1.1]
    assert actual == expected
