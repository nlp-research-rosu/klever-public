def iscube(a):
    a = abs(a)
    # Operational-sensitivity mutation: this materially changes the expression
    # that the claim executes from a ** (1 / 3) to a ** (2 / 3).
    return int(round(a ** (2 / 3))) ** 3 == a
