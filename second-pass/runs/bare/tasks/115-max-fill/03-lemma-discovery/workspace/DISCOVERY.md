# Trust-boundary discovery

The canonical inventory contains six rules, in `VERIFICATION`, and all six are
classified as `DEFINITION`.

- The two `water` rules are the base and recursive equations for the
  mathematical sum of a row.
- The two `requiredBuckets` rules are the base and recursive equations for the
  sum of per-row ceiling divisions. The positive-capacity condition is part of
  the recurrence's domain, not a separately asserted mathematical lemma.
- `functionsOf(Module(SS)) => collectFunctions(SS)` is a structural helper
  defining how the proof obtains a function map from a translated module.
- `solutionFunctions => functionsOf(solutionProgram)` is a named proof-term
  expansion tying that helper to the finalized translated program.

None of these rules is an `OPERATIONAL_RULE`: they do not advance the
small-step execution configuration or observe a runtime step. The operational
interpreter rules are in `semantic.k`, while the launcher-provided canonical
inventory exhaustively lists only the six rules above.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory.

The Stage 1 ordering is decisive. `prove.sh` first runs:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
```

That compilation places all six inventory rules into
`verification-kompiled`. Only afterward does the script run:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Thus no inventory rule is first proved against a module that omits that exact
rule. `spec.k` does contain three proved claims—the row-helper claim, the
grid-helper claim, and the end-to-end entry-point claim—but none is an
inventory rule with an exact reusable-rule correspondence. Comments calling
the first two claims “Lemma 1” and “Lemma 2” do not change this ordering.

## Domain lemmas

The domain-lemma set is empty. The inventory adds no mathematical fact beyond
the defining recurrences and structural/named proof-term expansions. It also
contains no rule carrying the `simplification` attribute.
