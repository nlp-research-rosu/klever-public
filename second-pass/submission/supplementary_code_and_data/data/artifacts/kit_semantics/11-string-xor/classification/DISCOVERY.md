# Rule trust-boundary discovery

The canonical inventory hash is
`5e9c7b1c2b4daaa9312cf8a80808008c934a4e555de06984522d3c157876a61d`.
All 13 canonical rules are classified exactly once and remain in inventory
order in `trust-boundary.json`.

## Definitions

The first twelve inventory rules all carry `simplification` and are classified
as `DEFINITION`.

- The four `xorAcc` rules are the two truncating base equations and the
  equal-head/unequal-head recurrences for the accumulated output.
- The two `bitString` rules structurally define the valid-input predicate.
- The three `lastX` rules define the final left-hand loop-target value for an
  empty or truncating zip and for the recursive paired case.
- The three `lastY` rules analogously define the final right-hand loop-target
  value.

These are equations or structural recurrences for named proof terms. They do
not observe or advance the Python configuration, and none asserts an
additional algebraic theorem beyond its definition.

## Separately proved derived lemma

Exactly one rule is classified as `PROVED_DERIVED_LEMMA`:

`rule-26fc544a3a34446e7dde0573f648e03f5ed33bc32ff9f6826cbd2730d9208ef4`.

It is the priority-40 loop summary rule in module `VERIFICATION`. The mounted
Stage 1 evidence establishes the required derivation:

1. `spec.k` states `LOOP-SPEC.loop-invariant` while importing only
   `VERIFICATION-BASE`.
2. `verification.k` places the reusable priority rule only in
   `VERIFICATION`, not in `VERIFICATION-BASE`.
3. `check_artifacts.py` normalizes the rule and the loop claim, asserts exact
   equality, and reports `bridge_matches_connection_claim=true`.
4. `prove.sh` compiles `verification-base-kompiled` with main module
   `VERIFICATION-BASE`, then runs:

   ```bash
   kprove spec.k \
     --definition verification-base-kompiled \
     --spec-module LOOP-SPEC \
     --claims LOOP-SPEC.loop-invariant
   ```

   Stage 1 records `#Top` and exit status 0 for this bridge-free proof.
5. Only afterward does `prove.sh` run the dependent entry proof against
   `verification-kompiled`:

   ```bash
   kprove spec.k \
     --definition verification-kompiled \
     --spec-module SPEC \
     --claims SPEC.string-xor
   ```

   Stage 1 also records `#Top` and exit status 0 for that command.

Thus the reusable rule has the same complete statement as a theorem first
proved against a module closure that does not contain the rule.

## Operational and domain lemmas

No canonical rule is classified as `OPERATIONAL_RULE`. The sole rule that
accelerates execution meets the stricter separately-proved-derived-lemma
criterion above.

The `DOMAIN_LEMMA` set is explicitly empty. Every simplification rule is a
defining equation or recurrence, so no additional trusted mathematical fact is
needed to close the proof.
