from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Generator, List, Optional, Type


@dataclass
class SelectorGroup:
    query: str

    @property
    def is_attribute_selector(self) -> bool:
        return self.query.startswith("[")

    @property
    def is_element_selector(self) -> bool:
        return not self.is_attribute_selector

    def to_element_selector(self) -> ElementSelector:
        return ElementSelector(self.query)

    def to_attribute_selector(self) -> AttributeSelector:
        return AttributeSelector(self.query)


@dataclass
class ElementSelector(SelectorGroup):
    element_type: Type[ast.AST] = field(init=False)
    attr_selectors: List[AttributeSelector] = field(init=False)

    def __post_init__(self) -> None:
        self.element_type = getattr(ast, self.query)
        self.attr_selectors = []

    def append_attr_selector(self, selector: SelectorGroup) -> None:
        self.attr_selectors.append(selector.to_attribute_selector())

    def find_nodes(self, tree: ast.AST) -> Generator[ast.AST, None, None]:
        for node in ast.walk(tree):
            if isinstance(node, self.element_type):
                everything_valid = all(attr.matches(node) for attr in self.attr_selectors)
                if everything_valid:
                    yield node


@dataclass
class AttributeSelector(SelectorGroup):
    attr: str = field(init=False)
    condition: str = field(init=False)
    val: str = field(init=False)

    def __post_init__(self) -> None:
        self.query = self.query.lstrip("[").rstrip("]")
        self.attr, self.condition, self.val = self.query.split()

    def matches(self, node: ast.AST) -> bool:
        if hasattr(node, self.attr):
            # TODO: consider = (equals)
            # TODO: consider explicit None type
            attr_val = getattr(node, self.attr)
            expected_val_type = getattr(ast, self.val, type(None))

            if isinstance(attr_val, expected_val_type):
                return True

        return False


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

    def _resolve_query(self) -> Generator[ElementSelector, None, None]:
        r = re.match(r"([A-Z]\w+)(\[[a-zA-Z0-9_= ]+\])*", self.query)
        el_selector: Optional[ElementSelector] = None

        if r:
            for g in r.groups():
                if g:
                    selector = SelectorGroup(g)

                    if selector.is_element_selector:
                        el_selector = selector.to_element_selector()
                    elif el_selector is not None:
                        el_selector.append_attr_selector(selector)

        if el_selector:
            yield el_selector

    def _resolve(self) -> Generator[ast.AST, None, None]:
        groups = list(self._resolve_query())
        single_group = groups[0]
        yield from single_group.find_nodes(self.tree)

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
