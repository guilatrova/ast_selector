def main(raw_selector: str):
    """
    CSS Selector:

    Raise = instance type
    > [el] = direct child
    .abc = ????
    #abc = ????
    [attr is X] = any element where attr is X
    [attr is None] = any element where attr is X
    [a=c][b=d] = combine attr selectors
    """
    selector_array = raw_selector.split()


if __name__ == "__main__:
    raw_selector = input("Selector:")
    main(raw_selector)
