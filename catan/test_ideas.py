tree = (0, (1, None, (2, (3, None, None), (4, (5, None, None), None))),
        (6, None, (7, (8, (9, None, None), None), None)))

def visit(tree):  # 
    print('one step of recursion')
    if tree is not None:
        try:
            value, left, right = tree
        except ValueError:  # wrong number to unpack
            print("Bad tree:", tree)
        else:  # The following is one of 3 possible orders.

            yield from visit(left)
            yield value  # Put this first or last for different orders.
            yield from visit(right)

print(list(visit(tree)))
