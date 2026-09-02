# Proof notes

`semantic.k` defines the constructor grammar consumed from `solution.mpy` and
an operational call machine for exactly the Python forms used by the solution:
function definitions, local parameters, returns, conditionals, integer
arithmetic and comparisons, lists, and one- or two-argument calls.

`spec.k` contains 26 positive claims.  Thirteen execute the exact translated
function bodies and check exact output lists; thirteen independently check the
natural-language contract on those executions: the factors multiply to the
input, are nondecreasing, and are prime.  The cases cover 1, primes, prime
powers, repeated factors, mixed composites, and all three prompt examples.

The installed Haskell backend does not support function-root claims and its
proof frontend throws an internal `ConcretizeCells` exception for this
definition's cell-root claims.  It also does not split symbolic conditions in
partial-function simplification.  Consequently the positive suite is a broad
ground proof partition rather than a universally quantified induction over
all positive integers.  `mutation-spec.k` is an expected-failure check showing
that the semantics rejects the incorrect result `[2, 5]` for input 70.
