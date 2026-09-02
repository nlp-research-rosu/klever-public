# Proof — `sum()` over a symbolic list (the fold builtin narrows)

Demonstrates that the `sum` builtin — now a **`<k>`-cell fold over `iterNext`**
(`src/mpy-builtins.k`), no longer a `[function]` — narrows a **symbolic** list in a
proof, exactly the way the for-loop invariants do.

`verification.k` defines the summary `sumOf(VS, ACC)` (a structural left fold,
`Val`-head + `projectIntTotal` cast — the loop-break `prefixSum` pattern). `spec.k`
proves two `[all-path]` claims over a symbolic `List[int]` `VS` (`requires allInt(VS)`):

1. **fold invariant** (circularity) — `sumAcc(list(VS), ACC)` folds to `sumOf(VS, ACC)`;
2. **entry** — the builtin call `sum(list(VS))` dispatches through `#bargs` to the
   fold and yields `sumOf(VS, 0)`.

`kprove` → **`#Top`** (both claims). Non-vacuous: corrupting a postcondition to
`… +Int 1` fails the implication check (0 `#Top`, 0 parse errors).

## Why it narrows (and a `[function]` would not)

`sum` folds by driving `iterNext` on the `<k>` cell:
`sumAcc(IT) => iterNext(IT) ~> sumCont(ACC)`. Because `iterNext` is a `<k>`-cell
rewrite, kprove **unifies** the symbolic `list(VS)` with `list(vCons(V,R))` /
`list(.ValSeq)`, substituting `VS`'s structure so `sumOf(VS, ACC)` reduces. The old
`sumFold` `[function]` on a symbolic `list(VS)` is match-only and gets stuck — see
[`reference/notes/iter-probe/`](../../../notes/iter-probe/INVESTIGATION.md).

The element rule matches `V:Val` and casts (`{V}:>Int`, with `isInt(V)` supplied by
`allInt`), because a bare `Int` pattern will not match a symbolic `Val` even when
`isInt(V)` holds — the same element-cast the loop invariants use.
