from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generator, Iterator, List, Optional, Type, Union

from .exceptions import UnableToReferenceQuery


@dataclass
class NavigationReference:
    reference_table: Dict[str, List[ast.AST]] = field(default_factory=lambda: defaultdict(list))

    def _build_reference(self, selector_group: SelectorGroup) -> str:
        if selector_group.is_element_selector:
            return f"${selector_group.query}"

        elif selector_group.is_drill_selector:
            last_ref = list(self.reference_table.keys())[-1]
            return f"${last_ref}.{selector_group.query}"

        raise UnableToReferenceQuery(selector_group.query)

    def get_last_entry(self) -> List[ast.AST]:
        return list(self.reference_table.values())[-1]

    def append(self, selector_group: SelectorGroup, val: ast.AST) -> None:
        ref = self._build_reference(selector_group)
        self.reference_table[ref].append(val)

    def get_reference(self, ref: str) -> Optional[List[ast.AST]]:
        k = list(reversed(self.reference_table.keys()))
        if ref in k:
            return self.reference_table[ref]

        return None


@dataclass
class SelectorGroup:
    navigation: NavigationReference
    query: str
    referentiable = True

    @property
    def is_attribute_selector(self) -> bool:
        return self.query.startswith("[")

    @property
    def is_drill_selector(self) -> bool:
        return self.query.startswith(".")

    @property
    def is_reference_selector(self) -> bool:
        return self.query.startswith("$")

    @property
    def is_parent_selector(self) -> bool:
        return self.query == ".."

    @property
    def is_element_selector(self) -> bool:
        return all(
            [
                not self.is_attribute_selector,
                not self.is_drill_selector,
                not self.is_reference_selector,
                not self.is_parent_selector,
            ]
        )

    def to_element_selector(self) -> ElementSelector:
        if self.is_element_selector:
            return ElementSelector(self.navigation, self.query)

        if self.is_parent_selector:
            return ParentSelector(self.navigation, self.query)

        if self.is_drill_selector:
            return DrillSelector(self.navigation, self.query)

        if self.is_reference_selector:
            return ReferenceSelector(self.navigation, self.query)

        raise TypeError()

    def to_attribute_selector(self) -> AttributeSelector:
        return AttributeSelector(self.navigation, self.query)

    def _find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        raise NotImplementedError()

    def find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        for node in self._find_nodes(branches):
            if self.referentiable:
                self.navigation.append(self, node)

            yield node


@dataclass
class ElementSelector(SelectorGroup):
    element_type: Type[ast.AST] = field(init=False)
    attr_selectors: List[AttributeSelector] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.element_type = getattr(ast, self.query)

    def append_attr_selector(self, selector: SelectorGroup) -> None:
        self.attr_selectors.append(selector.to_attribute_selector())

    def _matches(self, node: ast.AST) -> bool:
        return all(attr.matches(node) for attr in self.attr_selectors)

    def _find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        for tree in branches:
            for node in ast.walk(tree):
                node.parent = getattr(node, "parent", tree)  # type: ignore

                for child in ast.iter_child_nodes(node):
                    child.parent = node  # type: ignore

                if isinstance(node, self.element_type):
                    if self._matches(node):
                        yield node


@dataclass
class DrillSelector(ElementSelector):
    iteration: dict[Any, int] = field(default_factory=lambda: defaultdict(int))

    def __post_init__(self) -> None:
        self.element_type = ast.AST
        self.query = self.query.lstrip(".")

    def _get_drilled_instances(self, parent: ast.AST, node: Any) -> Generator[ast.AST, None, None]:
        drilled_instances: list[ast.AST] = []

        if isinstance(node, ast.AST):
            drilled_instances = [node]
        elif isinstance(node, list):
            drilled_instances = [valid for valid in node if isinstance(valid, ast.AST)]

        for drilled in drilled_instances:
            if self._matches(drilled):
                drilled.parent = parent  # type: ignore
                yield drilled

    def _find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        for node in list(branches):
            if self.query.isnumeric():
                attr_idx = int(self.query)
                if attr_idx == self.iteration[node.parent]:  # type: ignore
                    yield node

            elif drilled := getattr(node, self.query, False):
                yield from self._get_drilled_instances(node, drilled)

            self.iteration[node.parent] += 1  # type: ignore


class AttributeSelectorComparator(str, Enum):
    INSTANCE = " is "
    EQUALS = "="


@dataclass
class AttributeSelector(SelectorGroup):
    attr: str = field(init=False)
    condition: AttributeSelectorComparator = field(init=False)
    val: str = field(init=False)
    iteration: dict[Any, int] = field(default_factory=lambda: defaultdict(int))

    def __post_init__(self) -> None:
        self.query = self.query.lstrip("[").rstrip("]")
        if AttributeSelectorComparator.EQUALS in self.query:
            self.condition = AttributeSelectorComparator.EQUALS
        else:
            self.condition = AttributeSelectorComparator.INSTANCE

        self.attr, self.val = [x.strip() for x in self.query.split(self.condition)]

    def _match_equals(self, node: ast.AST) -> bool:
        attr_val = str(getattr(node, self.attr))
        expected_val = self.val

        return attr_val == expected_val

    def _match_instance(self, node: ast.AST) -> bool:
        if self.attr.isdigit():
            attr_idx = int(self.attr)
            if attr_idx != self.iteration[node.parent]:  # type: ignore
                return False

            attr_val = node
        else:
            attr_val = getattr(node, self.attr)

        expected_val_type = getattr(ast, self.val, type(None))

        if isinstance(attr_val, expected_val_type):
            return True

        return False

    def matches(self, node: ast.AST) -> bool:
        if self.condition == AttributeSelectorComparator.INSTANCE:
            result = self._match_instance(node)
        else:
            result = self._match_equals(node)

        self.iteration[node.parent] += 1  # type: ignore
        return result


@dataclass
class ReferenceSelector(ElementSelector):
    referentiable = False

    def __post_init__(self) -> None:
        self.element_type = ast.AST

    def _walk_parent(self, node: ast.AST) -> Generator[ast.AST, None, None]:
        cur_node = node
        while cur_node.parent and cur_node != cur_node.parent:  # type: ignore
            yield cur_node.parent  # type: ignore
            cur_node = cur_node.parent  # type: ignore

    def _find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        tree = list(branches)  # Force generators to build reference table until this point
        references = self.navigation.get_reference(self.query) or []

        for ref in references:
            if any((node for node in tree if ref in self._walk_parent(node))):
                if self._matches(ref):
                    yield ref


@dataclass
class ParentSelector(ReferenceSelector):
    def _find_nodes(self, branches: Union[Iterator[ast.AST], ast.AST]) -> Generator[ast.AST, None, None]:
        if not isinstance(branches, Iterator):
            branches = iter([branches])

        for node in branches:
            yield node.parent  # type: ignore
