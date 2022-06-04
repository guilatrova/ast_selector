# AST Selector

<p align="center">
    <img src="https://raw.githubusercontent.com/guilatrova/ast_selector/main/img/logo.png">
</p>

<h2 align="center">Query AST elements by using CSS Selector-like syntax</h2>

<p align="center">
  <a href="https://github.com/guilatrova/ast_selector/actions"><img alt="Actions Status" src="https://github.com/guilatrova/ast_selector/workflows/CI/badge.svg"></a>
  <a href="https://pypi.org/project/ast-selector/"><img alt="PyPI" src="https://img.shields.io/pypi/v/ast_selector"/></a>
  <img src="https://badgen.net/pypi/python/ast_selector" />
  <a href="https://github.com/relekang/python-semantic-release"><img alt="Semantic Release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg"></a>
  <a href="https://github.com/guilatrova/ast_selector/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/guilatrova/ast_selector"/></a>
  <a href="https://pepy.tech/project/ast-selector/"><img alt="Downloads" src="https://static.pepy.tech/personalized-badge/ast_selector?period=total&units=international_system&left_color=grey&right_color=blue&left_text=%F0%9F%A6%96%20Downloads"/></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
  <a href="https://github.com/guilatrova/tryceratops"><img alt="try/except style: tryceratops" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black" /></a>
  <a href="https://twitter.com/intent/user?screen_name=guilatrova"><img alt="Follow guilatrova" src="https://img.shields.io/twitter/follow/guilatrova?style=social"/></a>
</p>

> "Query AST elements 🌲 by using CSS Selector-like 💅 syntax."

## Installation and usage

### Installation

```
pip install ast_selector
```

### Usage

```py
from ast_selector import AstSelector

tree = load_python_code_as_ast_tree()
query = "FunctionDef Raise $FunctionDef"
# Query all functions that raises at least an exception

functions_raising_exceptions = AstSelector(query, tree).all()
```

### Use Cases

#### Functions that return int

```py
from ast_selector import AstSelector

tree = load_python_code_as_ast_tree()
query = "FunctionDef.returns[id=int] $FunctionDef"
# Query all functions that return ints e.g. def sum() -> int

function_element = AstSelector(query, tree).first()
```

## License

MIT

## Credits

It's extremely hard to keep hacking on open source like that while keeping a full-time job. I thank God from the bottom of my heart for both the inspiration and the energy.
