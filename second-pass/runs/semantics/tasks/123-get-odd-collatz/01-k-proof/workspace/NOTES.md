# Verification scope

`spec.k` proves the implementation at the semantic transition boundary:

- `odd-step` symbolically proves, for every positive odd loop value greater
  than one and every accumulated value sequence, that the program appends that
  value and changes `n` to `3*n+1`.
- `even-step` symbolically proves, for every positive non-odd loop value greater
  than one, that the accumulator is unchanged and `n` changes according to the
  supplied semantics' Python floor division.
- `exit-step` symbolically proves, for every accumulated sequence at `n == 1`,
  that the program appends `1` and returns `sortVS` of the complete sequence.
- Four end-to-end claims prove complete executions for `1`, `5`, `6`, and `7`.
  The LLVM assertion harness additionally executes the 111-step trace from
  `27`.

Together, the three symbolic claims are a partial-correctness proof for every
finite Collatz trace: induction on the number of loop transitions composes
`odd-step`/`even-step` with `exit-step`. The supplied semantics models
`sorted` by its documented trusted `sortVS` primitive in symbolic proofs and
by insertion sort in the LLVM runtime.

A universal termination theorem for every positive integer is intentionally
not claimed. Such a theorem would settle the Collatz conjecture, which remains
open; K reachability proves the function's result on executions that reach
`1`.
