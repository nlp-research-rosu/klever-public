# Each proof-local arithmetic bridge is exercised, followed by an observable
# assignment.  The bridge-free and bridge-enabled final configurations must be
# byte-equivalent as canonical JSON.
x = -5 % 2
y = 10 + -3
z = -3 * 4
flag = 99

assert x == 1
assert y == 7
assert z == -12
assert flag == 99
