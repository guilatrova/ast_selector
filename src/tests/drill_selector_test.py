import ast
import pytest  # noqa: F401

from ast_selector import AstSelector

from .helpers import read_sample


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


def test_filter_drill_properties():
    """
    Drill ability:

    if Expr has value and value is Call
    -> then take value from Expr

    if Expr.value has func and func is Attribute
    -> then take func from Expr.value
    """
    tree = read_sample("log_object")
    query = "Expr[value is Call].value[func is Attribute].func"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.Attribute)


def test_drill_filter_child_array():
    tree = read_sample("func_pass")
    query = "FunctionDef.body[0 is Pass].0"

    selector = AstSelector(query, tree)
    found = selector.all()

    assert len(found) == 1
    assert isinstance(found[0], ast.Pass)


# TODO: Support element wildcard (*)
# TODO: Support deeper references (e.g. $FunctionDef.1 when FunctionDef(not this) FunctionDef(this))
# TODO: Support direct children (e.g. FunctionDef > FunctionDef using ast.iter_children instead of ast.walk)
# TODO: Support OR operations
