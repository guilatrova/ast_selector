import ast
import pytest  # noqa: F401

from ast_selector import AstSelector

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


def test_drill_properties_get_first():
    """
    Drill ability + Get origin:

    Drill 2 levels and get first reference
    """
    tree = read_sample("log_object")
    query = "Expr[value is Call].value[func is Attribute].func $Expr"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.Expr)
    assert isinstance(found.value, ast.Call)
    assert isinstance(found.value.func, ast.Attribute)


def test_drill_properties_get_second():
    """
    Drill ability + Get origin:

    Drill 2 levels and get second reference
    """
    tree = read_sample("log_object")
    query = "Expr[value is Call].value[func is Attribute].func $Expr.value"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.Call)
    assert isinstance(found.func, ast.Attribute)


def test_filter_functions_returning_str():
    tree = read_sample("funcs")
    query = "FunctionDef.returns[id=str].."

    selector = AstSelector(query, tree)
    found = selector.all()

    assert len(found) == 1
    assert isinstance(found[0], ast.FunctionDef)


def test_filter_functions_returning_int():
    tree = read_sample("funcs")
    query = "FunctionDef.returns[id=int] $FunctionDef"

    selector = AstSelector(query, tree)
    found = selector.all()

    assert len(found) == 2
    assert all(isinstance(x, ast.FunctionDef) for x in found)


def test_filter_functions_returning_int_with_name():
    tree = read_sample("funcs")
    query = "FunctionDef.returns[id=int] $FunctionDef[name=main_int]"

    selector = AstSelector(query, tree)
    found = selector.all()

    assert len(found) == 1
    assert found[0].name == "main_int"


def test_drill_function_returning_int():
    tree = read_sample("funcs")
    query = "FunctionDef.returns[id=int] $FunctionDef.args"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.arguments)


def test_reference_nonexisting_match():
    tree = read_sample("funcs")
    query = "Raise $Raise"

    selector = AstSelector(query, tree)

    assert selector.exists() is False
    assert selector.count() == 0


def test_drill_list_ast_from_reference():
    """
    1. Drill from Expr, to value.func
    2. Reference $Expr.value
    3. Drill to .args
    """
    tree = read_sample("log_object")
    query = "Expr[value is Call].value[func is Attribute].func[attr = exception] $Expr.value.args"

    selector = AstSelector(query, tree)
    found = selector.all()

    assert all(isinstance(x, ast.AST) for x in found)


def test_long_navigation_get_back_to_original_reference():
    tree = read_sample("log_object")
    query = "FunctionDef Expr[value is Call].value[func is Attribute].func[attr = exception] $FunctionDef"

    selector = AstSelector(query, tree)
    found = selector.first()

    assert isinstance(found, ast.FunctionDef)


# TODO: Support array (e.g. FunctionDef.body.0)
# TODO: Support direct children (e.g. FunctionDef > FunctionDef using ast.iter_children instead of ast.walk)
# TODO: Support deeper references (e.g. FunctionDef[1] when FunctionDef(not this) FunctionDef(this))
# TODO: Support OR operations
# TODO: Support element wildcard (*)
