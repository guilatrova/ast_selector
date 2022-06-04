class AstSelectorException(Exception):
    pass


class UnableToFindElement(AstSelectorException):
    def __init__(self, query: str) -> None:
        super().__init__(f"Unable to find element with query '{query}' in specified tree")
