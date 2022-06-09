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

**Summary**
- [Installation and usage](#installation-and-usage)
  - [Installation](#installation)
  - [Usage](#usage)
- [Examples](#examples)
  - [Query by AST type](#query-by-ast-type)
  - [Filter AST by property type](#filter-ast-by-property-type)
  - [Drill to AST property](#drill-to-ast-property)
  - [Filter AST by property value](#filter-ast-by-property-value)
  - [Filter AST by multiple conditions](#filter-ast-by-multiple-conditions)
  - [Drill down but take previous reference](#drill-down-but-take-previous-reference)
  - [Filter and drill through references](#filter-and-drill-through-references)
  - [Count functions](#count-functions)
  - [Take first node only](#take-first-node-only)
  - [Check if node exists](#check-if-node-exists)
- [Contributing](#contributing)
- [Change log](#change-log)
- [License](#license)
- [Credits](#credits)

## Installation and usage

### Installation

```
pip install ast-selector
```

### Usage

```py
from ast_selector import AstSelector

tree = load_python_code_as_ast_tree()
query = "FunctionDef Raise $FunctionDef"
# Query all functions that raises at least an exception

functions_raising_exceptions = AstSelector(query, tree).all()
```

## Examples

### Query by AST type

Simply use the AST type. Note it should have the proper casing.

```py
AstSelector("FunctionDef", tree).all() # Any Ast.FunctionDef
AstSelector("Raise", tree).all() # Any ast.Raise
AstSelector("Expr", tree).all() # Any ast.Expr
```

### Filter AST by property type

You can filter property types by writing like: `[Prop is Type]`.

Condition: Any `ast.Expr` that contains `.value` prop and that prop is an instance of `ast.Call`

Result: List of `ast.Expr` that fulfills the condition.

```py
AstSelector("Expr[value is Call]", tree).all()
```

### Drill to AST property

You can navigate as you filter the elements you want by using `.prop`.

Condition: Any `ast.Expr` that contains `.value` prop and that prop is an instance of `ast.Call`, take `.value`.

Result: List of `ast.Call` that fulfills the condition.

```py
AstSelector("Expr[value is Call].value", tree).all()
```

### Filter AST by property value

You can filter property values by writing like: `[Prop = Value]`.

Condition: Any `ast.FunctionDef`, take `returns` as long as it contains `id` equals to `int`.

Result: List of `ast.Name` that fulfills the condition.

```py
AstSelector("FunctionDef.returns[id=int]", tree).all()
```

### Filter AST by multiple conditions

You can keep appending `[Cond1][Cond2][Cond3]` as you wish:

Condition: Any `ast.Raise` that has `exc` of type `ast.Call` **AND** that has `cause` as `None`.

Result: List of `ast.Raise` that fulfills the condition.

```py
AstSelector("Raise[exc is Call][cause is None]", tree).all()
```

### Drill down but take previous reference

You can keep drilling down, but take a previous value as your result by using `$[Placeholder]` syntax:

Condition: Any `ast.FunctionDef`, take `returns` as long as it has `id` equals to `int`, then take the original `FunctionDef`.

Result: List of `ast.FunctionDef` that fulfills the condition.

```py
AstSelector("FunctionDef.returns[id=int] $FunctionDef", tree).all()
```

### Filter and drill through references

You can keep filtering and drilling references as you would normally.

Drill `$Expr` and take `args` as result:

```py
AstSelector("Expr[value is Call].value[func is Attribute].func[attr = exception] $Expr.value.args", tree).all()
```

Drill `$FunctionDef` (redundant) and filter functions named `main_int` as result:

```py
AstSelector("FunctionDef.returns[id=int] $FunctionDef[name=main_int]", tree).all()
```

### Count functions

```py
AstSelector(query, tree).count()
```

### Take first node only

```py
AstSelector(query, tree).first()  # Raises exception if None
```

### Check if node exists

```py
AstSelector(query, tree).exists()
```

## Contributing

Thank you for considering making AST Selector better for everyone!

Refer to [Contributing docs](docs/CONTRIBUTING.md).

## Change log

See [CHANGELOG](CHANGELOG.md).

## License

MIT

## Credits

It's extremely hard to keep hacking on open source like that while keeping a full-time job. I thank God from the bottom of my heart for both the inspiration and the energy.
