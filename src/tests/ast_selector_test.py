from ast_selector.main import AstSelector

from .helpers import read_sample


def test_find_element():
    tree = read_sample("except_reraise_no_cause")
    query = "Raise"

    selector = AstSelector(query, tree)

    assert selector.exists() is True


def test_count_elements():
    tree = read_sample("except_reraise_no_cause")
    query = "Raise"

    selector = AstSelector(query, tree)

    assert selector.count() == 3


def test_find_raise_with_single_attr():
    tree = read_sample("except_reraise_no_cause")
    query = "Raise[exc is Call]"

    selector = AstSelector(query, tree)

    assert selector.exists() is True


# Further tests:
# query = "ExceptHandler Raise[exc is Call]"
# query = "ExceptHandler Raise[exc is Call][cause is None]"
