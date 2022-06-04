class AstSelectorException(Exception):
    pass


class UnableToFindElement(AstSelectorException):
    def __init__(self, query: str) -> None:
        self.query = query
        super().__init__(f"Unable to find element with query '{query}' in specified tree")


class UnableToReferenceQuery(AstSelectorException):
    def __init__(self, query: str) -> None:
        self.query = query
        super().__init__(f"Unable to reference '{query}'")
