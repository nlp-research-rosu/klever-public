# numeric-while digit-sum probe

De-risks the **numeric-while partial-correctness rung** on the unified semantics: the digit-sum
loop `while n > 0: r += n % 10; n = n // 10` proves `#Top` via the `digitAcc(N, R)` while-invariant.

Key: the summary must match the reference's `//`/`%`, which are `pyMod`-based:
`digitAcc(N, R) => digitAcc((N - pyMod(N,10)) /Int 10, R + pyMod(N,10)) requires N > 0`.
The `[all-path]` circularity folds one unroll (case-split N>0 / N<=0); final `n` is existential
(`?_:Int`), only `r := digitAcc(N, R)` is pinned. Opens Q94 skjkasdkd (digit sum of the max prime).
