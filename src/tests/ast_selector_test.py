from ast_selector import AstSelector

from .helpers import read_sample


def test_find_raise_with_single_attr():
    tree = read_sample("except_reraise_no_cause")
    query = "Raise[exc is Call]"

    selector = AstSelector(query, tree)

    assert selector.exists() is True


# Further tests:
# query = "ExceptHandler Raise[exc is Call]"
# query = "ExceptHandler Raise[exc is Call][cause is None]"
