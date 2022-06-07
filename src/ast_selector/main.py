from __future__ import annotations

import ast
import itertools
import re
from typing import Generator, List, Optional

from .exceptions import UnableToFindElement
from .models import ElementSelector, NavigationReference, SelectorGroup


class AstSelector:
    """
    CSS(Ast) Selector:

    Raise = instance type
    > [el] = direct child
    .abc = ????
    #abc = ????
    [attr is X] = any element where attr is X
    [attr is None] = any element where attr is X
    [a=c][b=d] = combine attr selectors
    """

    def __init__(self, query: str, tree: ast.AST) -> None:
        self.tree = tree
        self.query = query
        # TODO: Validate query

    def _resolve_query(self) -> List[ElementSelector]:
        PARENT_RE = r"(\.\.)?"
        DRILL_RE = r"(\.\w+)?"
        ATTR_RE = r"(\[[a-zA-Z0-9_= ]+\])?"
        NODE_RE = r"(\$?[A-Z]\w+)?"

        reg = re.findall(f"{PARENT_RE}{DRILL_RE}{ATTR_RE}{NODE_RE}", self.query)
        reggroup = [x for x in itertools.chain(*reg) if x]

        el_selector: Optional[ElementSelector] = None
        reference_table = NavigationReference()
        results = []

        for g in reggroup:
            selector = SelectorGroup(reference_table, g)

            if selector.is_attribute_selector:
                if el_selector is not None:
                    el_selector.append_attr_selector(selector)
            else:
                el_selector = selector.to_element_selector()
                results.append(el_selector)

        return results

    def _resolve(self) -> Generator[ast.AST, None, None]:
        groups = self._resolve_query()

        tree = iter([self.tree])
        for group in groups:
            tree = group.find_nodes(tree)

        yield from tree

    def exists(self) -> bool:
        el = self._resolve()
        try:
            next(el)
        except StopIteration:
            return False
        else:
            return True

    def count(self) -> int:
        nodes = self._resolve()
        return len(list(nodes))

    def all(self) -> List[ast.AST]:
        nodes = self._resolve()
        return list(nodes)

    def first(self) -> ast.AST:
        el = self._resolve()
        try:
            first = next(el)
        except StopIteration as e:
            raise UnableToFindElement(self.query) from e
        else:
            return first
