# Proof — `x in list` over a symbolic list (the membership fold narrows)

`x in list` is now a **`<k>`-cell fold over `iterNext`** (`src/mpy-operators.k`,
`#memberAcc`/`#memberCont`), not the `valInSeq` `[function]`. Being a `<k>`-cell
rewrite it narrows a **symbolic** list, like `all`/`any`.

`verification.k` defines `memberOf(V, VS)` with the **same branch shape** as the
fold (found on head-match, else recurse — a single `orBool` rule won't reduce
under the fold's branch condition). `spec.k` proves:

```k
claim <k> #memberAcc(V, list(VS)) => ?R:Bool ... </k> ensures ?R ==Bool memberOf(V, VS) [all-path]
```

`kprove` → **`#Top`**, non-vacuous (negating the postcondition fails the
implication, 0 parse errors).

Note: only **list** membership is a fold. `str` `in` is a **substring** search
(a different operation) and `tuple` has no `in`, so both stay in `applyCmp`.
