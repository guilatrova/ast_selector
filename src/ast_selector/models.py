from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Generator, Iterator, List, Type, Union


@dataclass
class SelectorGroup:
    query: str

    @property
    def is_attribute_selector(self) -> bool:
        return self.query.startswith("[")

    @property
    def is_drill_selector(self) -> bool:
        return self.query.startswith(".")

    @property
    def is_element_selector(self) -> bool:
        return not self.is_attribute_selector and not self.is_drill_selector

    def to_element_selector(self) -> ElementSelector:
        return ElementSelector(self.query)

    def to_attribute_selector(self) -> AttributeSelector:
        return AttributeSelector(self.query)

    def to_drill_selector(self) -> DrillSelector:
        return DrillSelector(self.query)


@dataclass
class ElementSelector(SelectorGroup):
    element_type: Type[ast.AST] = field(init=False)
    attr_selectors: List[AttributeSelector] = field(init=False)

    def __post_init__(self) -> None:
        self.element_type = getattr(ast, self.query)
        self.attr_selectors = []

    def append_attr_selector(self, selector: SelectorGroup) -> None:
        self.attr_selectors.append(selector.to_attribute_selector())

    def find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        for tree in branches:
            for node in ast.walk(tree):
                if isinstance(node, self.element_type):
                    everything_valid = all(attr.matches(node) for attr in self.attr_selectors)
                    if everything_valid:
                        yield node


@dataclass
class DrillSelector(ElementSelector):
    def __post_init__(self) -> None:
        self.element_type = ast.AST
        self.attr_selectors = []
        self.query = self.query.lstrip(".")

    def find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        for node in list(branches):
            if drilled := getattr(node, self.query, False):
                if isinstance(drilled, ast.AST):
                    yield drilled


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
