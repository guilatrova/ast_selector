# Contributing

- [Contributing](#contributing)
  - [Setup](#setup)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Conventional Commits](#conventional-commits)

## Setup

Install the dependency manager (if not already done):

```sh
pip3 install poetry
```

Install all dependencies, pre-commit hooks, and git config:

```sh
poetry install
pre-commit install
git config commit.template .gitmessage
```

## Testing

You can either run:

```sh
❯ poetry run ❯ pytest
============================================================= test session starts =============================================================
platform linux -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/gui/Desktop/poc/ast_selector, configfile: pyproject.toml, testpaths: src/tests
plugins: cov-3.0.0
collected 18 items

src/tests/attr_selector_test.py ....                                                                                                    [ 22%]
src/tests/drill_selector_test.py ...                                                                                                    [ 38%]
src/tests/element_selector_test.py ..                                                                                                   [ 50%]
src/tests/reference_selector_test.py .........                                                                                          [100%]

============================================================= 18 passed in 0.03s ==============================================================
```

## Linting

If you installed `pre-commit` it should ensure you're not commiting anything broken.

You can run `./bin/lint` to check if there's any issue.

## Conventional Commits

We automate the versioning and release process! It's only possible if we are consistent with the commit pattern and follow the conventional commits standards.

Refer to [Conventional Commits here](https://www.conventionalcommits.org/en/v1.0.0/) and if you're curious to understand how the publishing works [check here](https://python-semantic-release.readthedocs.io/en/latest/).
