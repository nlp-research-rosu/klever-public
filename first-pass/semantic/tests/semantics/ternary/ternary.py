# IfExp ternary `T if C else E`: evaluates C, returns the chosen branch *value*
# (not a bool). py2mpy emits the condition first: IfExp(C, T, E).
assert (1 if True else 2) == 1
assert (1 if False else 2) == 2
assert ("yes" if 1 < 2 else "no") == "yes"

x = 5
assert (x if x > 0 else -x) == 5
y = -3
assert (y if y > 0 else -y) == 3

# nested ternary
assert (("a" if False else "b") if True else "c") == "b"

# condition can be a None test
z = None
assert (0 if z is None else z) == 0
