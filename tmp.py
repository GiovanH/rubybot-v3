def decorate(func):
    print(func)
    return func


@decorate
def p(e):
    print(e)

p(3)
