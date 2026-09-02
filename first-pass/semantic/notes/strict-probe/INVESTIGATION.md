# Do strict/seqstrict freezers disturb circularity proofs?

Question (stage 1 of the semantics cleanup): `strict`/`seqstrict` are frontend sugar for the
heat/cool sentinel pairs we hand-rolled — but the heated shapes are generated freezers, and our
whole proof method is circularities + structural narrowing. Go/no-go before converting the
reference. **Verdict: GO — the probe proves `#Top` first try.**

```sh
cd verification/humaneval/reference/notes/strict-probe
kompile verif-strict.k --backend haskell --main-module VERIF-STRICT --syntax-module VERIF-STRICT --output-definition verif-strict-kompiled
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 500 kprove spec-loop.k --definition verif-strict-kompiled --spec-module SPEC-LOOP-SPEC --depth 2000
```

The probe ([verif-strict.k](verif-strict.k)) exercises every strictness feature the conversion
needs, inside one below-zero-shaped loop over a symbolic cons list:

- `add`/`lt` `[seqstrict]` — heated operand evaluation (freezer shapes live inside one iteration);
- `ite` `[strict(1)]` — the `#branch` analog: after cooling, the two `ite(true,…)`/`ite(false,…)`
  rules CONDITIONALLY MATCH the symbolic Bool and case-split, exactly like the sentinel version;
- `KResult ::= Val` — heating stops at values (`isKResult` side conditions);
- the summary `clampSum` (declare-then-guard, case-split rules) folds through the circularity.

Claim: `<k> #sum(VS) => .K </k> <acc> A => clampSum(VS, A) </acc>` — [all-path], proves.

Reading: the freezers exist only BETWEEN circularity anchor points (the invariant anchors at
`#sum`, a plain rewrite sentinel); by the time the circularity applies or the implication check
runs, every heated expression has cooled to a value. Strictness changes the intermediate term
shapes, not the states the proof method touches. The conversion can proceed; the remaining port
burden is mechanical (interceptions matching `#binR`/`#cmpR`/`#applyK` shapes, and the
while-cluster specs if While is unrolled to If).
