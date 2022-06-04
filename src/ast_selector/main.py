from __future__ import annotations

import ast
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
        NODE_RE = r"(\$?[A-Z]\w+)"
        ATTR_RE = r"(\[[a-zA-Z0-9_= ]+\])*"
        DRILL_RE = r"(\.\w+)*"

        reggroup = re.findall(f"{NODE_RE}{ATTR_RE}{DRILL_RE}", self.query)
        el_selector: Optional[ElementSelector] = None
        reference_table = NavigationReference()
        results = []

        for reg in reggroup:
            for g in reg:
                if g:
                    selector = SelectorGroup(reference_table, g)

                    if selector.is_element_selector:
                        el_selector = selector.to_element_selector()
                        results.append(el_selector)

                    elif el_selector is not None:
                        if selector.is_attribute_selector:
                            el_selector.append_attr_selector(selector)
                        elif selector.is_reference_selector:
                            results.append(selector.to_reference_selector())
                        else:  # drill
                            results.append(selector.to_drill_selector())

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
