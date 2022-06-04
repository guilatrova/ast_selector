import ast

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


def test_find_raise_with_two_attrs():
    tree = read_sample("except_reraise_no_cause")
    query = "Raise[exc is Call][cause is None]"

    selector = AstSelector(query, tree)

    assert selector.exists() is True


def test_find_all_raise_below_except_handler():
    tree = read_sample("except_reraise_no_cause")
    query = "ExceptHandler Raise[exc is Call]"

    selector = AstSelector(query, tree)
    found = selector.all()

    assert len(found) == 1
    assert isinstance(found[0], ast.Raise)


def test_find_first_raise_below_except_handler():
    tree = read_sample("except_reraise_no_cause")
    query = "ExceptHandler Raise[exc is Call][cause is None]"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.Raise)


def test_find_drill_properties():
    """
    Drill ability:

    if Expr has value and value is Call
    -> then take value from Expr
    """
    tree = read_sample("log_object")
    query = "Expr[value is Call].value"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.Call)
