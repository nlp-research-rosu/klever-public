# Proof — `sum` over a symbolic `List[bool]` (bool is summed as 0/1)

Companion to `sum-fold` (`List[int]`). `sum`'s element step is a **single** `<k>`-cell
rule `… => sumAcc(R, ACC +Int intOf(V)) requires isInt(V) orBool isBool(V)` — one rule,
not two, so kprove never branches `isInt`-vs-`isBool` on a symbolic `V` (two rules would,
and that vacuous branch breaks the `List[int]` proof).

`intOf`'s int/bool split lives in `[simplification]` lemmas (`lemmas.k`) that fire only
when the element's sort is *entailed*:

```k
intOf(V) => projectIntTotal(V)                          requires isInt(V)   [simplification]
intOf(V) => #if projectBoolTotal(V) #then 1 #else 0 #fi requires isBool(V)  [simplification]
```

So a `List[bool]` (`requires allBool(VS)`) resolves each element through `projectBoolTotal`
(the Bool analog of `projectIntTotal`), and `sumAcc(list(VS), ACC)` folds to
`countTrue(VS, ACC)`. `kprove` → **`#Top`**, non-vacuous.

Takeaway: to add a new element type to a fold, add a `projectXTotal` cast + an `intOf`
`[simplification]` lemma — **not** another `<k>`-cell element rule.
