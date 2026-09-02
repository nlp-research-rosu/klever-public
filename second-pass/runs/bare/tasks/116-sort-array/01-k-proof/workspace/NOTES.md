# Verification notes

The prose contract says to order by `(number of 1 bits, decimal value)`, but
the three examples display ordinary numeric sorting.  Those conflict: for
example, the prose requires `[1, 5, 2, 3, 4]` to become
`[1, 2, 4, 3, 5]`.  The implementation and formal reference model follow the
prose because it defines the requested algorithm.  `spec.k` includes cases
that deliberately distinguish the two interpretations.

For negative integers (outside the stated non-negative domain), `int.bit_count`
counts bits in the magnitude.  Thus the documented negative example evaluates
to `[-4, -2, -6, -5, -3]` under the bit-count contract, not ordinary numeric
order.

The proof links the exact translated AST to an independent K reference model.
It proves popcount and comparator agreement for arbitrary integers, proves all
execution paths for symbolic arrays through length three, proves longer
representative end-to-end cases (including duplicates and negatives), and
checks ordering plus multiplicity preservation for the distinguishing example.
The six length-three claims partition every possible comparator path.  The
KORE equality check in `prove.sh` prevents the named AST used by the claims
from drifting away from freshly generated `solution.mpy`.
