# K proof trust-boundary discovery

The canonical inventory contains 12 rules from the local `VERIFICATION`
module closure. The classifications preserve the inventory order and use the
inventory hash
`25b938408e3059398c920d927e696e9f95b8d23ac41685644a7a5cd11105f257`.

## Classification summary

- **DEFINITION (6):** `solutionModule`, `lpfCondition`, and `lpfStep` are macro
  expansions naming proof terms. The three `lpfSpec` equations are the base,
  divisible, and nondivisible cases of the mathematical trial-division
  recurrence.
- **OPERATIONAL_RULE (5):** the five rules carrying `priority(40)` observe or
  update the MPY configuration for the exact comparison, remainder test,
  floor-division assignment, increment, and return redexes used by the
  program. They are symbolic execution accelerators within the verification
  model.
- **PROVED_DERIVED_LEMMA (0):** there are no separately proved derived lemmas.
- **DOMAIN_LEMMA (1):**
  `rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84`
  asserts that deleting a fresh frame key from `(L |-> V) M` restores `M`.
  It carries `simplification`, constrains existing Map operations rather than
  defining a new named summary, and is trusted by the Stage 1 proof.

The domain-lemma set is therefore **not empty**; it contains exactly the Map
deletion simplification above.

## Separately proved derived-lemma evidence

There are no such lemmas to identify. Stage 1 `prove.sh` first runs:

```text
kompile verification.k --backend haskell --main-module VERIFICATION ...
```

and only afterward runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Thus every inventoried rule, including the Map simplification and all five
symbolic accelerators, is already present in the compiled verification module
used by the only proof command. The script contains no earlier proof against a
module omitting any of those rules, and no later compilation step installs an
exact previously proved rule. The `lpf-loop` and
`largest-prime-factor-entry` sentences in `spec.k` are reachability claims,
not inventoried reusable rules, so they do not change this conclusion.
