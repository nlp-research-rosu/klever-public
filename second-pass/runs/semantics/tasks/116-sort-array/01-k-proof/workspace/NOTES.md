# Verification notes

The prose contract and the examples in `prompt.py` are inconsistent.

For example, `4` has one `1` in its binary representation and `3` has two, so
the stated rule requires `4` before `3`. The first and third examples instead
show ordinary decimal order. The negative example is outside the stated
non-negative domain.

The implementation and universal K claim follow the prose contract on
non-negative integers. The implementation first sorts by decimal value and
then applies the reference semantics' stable keyed sort using the binary
popcount. This is equivalent to sorting by `(popcount, decimal value)`. For a
conservative extension that also realizes the negative example, negative
integers receive the same key and therefore retain the preceding decimal
order.

`sortVS` and `sortKeyVS` are the trusted sorting primitives supplied by the
reference semantics. The universal claim proves the program reduces to their
composition with the exact popcount closure. A separate universal claim proves
that closure reduces to the supplied `bin`/`count` semantics for every
non-negative integer. Concrete LLVM assertions and an independent CPython
differential check exercise the trusted concrete sorting leg.
