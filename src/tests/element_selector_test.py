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


# TODO: Support element wildcard (*)
# TODO: Support direct children (e.g. FunctionDef > FunctionDef using ast.iter_children instead of ast.walk)
# TODO: Support OR operations
