import ast
import pytest  # noqa: F401

from ast_selector import AstSelector

from .helpers import read_sample


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
    assert selector.count() == 1


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
